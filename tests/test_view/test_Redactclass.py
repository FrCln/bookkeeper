from pytestqt.qt_compat import qt_api
from bookkeeper.view.Redactclass import MainTable, BudgetTable, CatChoice, RedactField, MyMainWindow


def data_for_testing():
    test_list = [[1, 4, 5, "Hello", "Bye"], ["No", 6, 10, 6, 7]]
    return test_list
    
def data_for_testing_last_row():
    test_row = ["hello", 3 , 3, "Key", "No"]
    return test_row
    
    
def test_table_fill_data(qtbot):
    widget = MainTable()
    qtbot.addWidget(widget)
    
    data = data_for_testing()
    widget.fill_data(data)
    
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            assert widget.item(i, j).text() == str(data[i][j])
            
    amount = widget.get_last_expense_sum()
    assert amount == widget.item(widget.rowCount() - 1, 1).text()
    
            
def test_table_insert_row(qtbot):
    widget = MainTable()
    qtbot.addWidget(widget)
            
    begin_cnt = widget.rowCount()
    widget.insert_row()
    end_cnt = widget.rowCount()
    assert end_cnt == begin_cnt + 1
    
def test_table_remove_row(qtbot):
    widget = MainTable()
    qtbot.addWidget(widget)
    
    begin_cnt = widget.rowCount()
    widget.remove_row()
    end_cnt = widget.rowCount()
    assert end_cnt == begin_cnt - 1
    
def test_table_fill_last_row(qtbot):
    widget = MainTable()
    qtbot.addWidget(widget)
    
    data = data_for_testing_last_row()
    
    widget.fill_row(data)
    for i in range(len(data)):
        assert widget.item(widget.rowCount() - 1, i).text() == str(data[i])
        
        
        
def test_add_delete_spending(qtbot):
    widget = BudgetTable()
    qtbot.addWidget(widget)
    
    amount_add = "1000"
    amount_del = 100
    cur_amounts_old = [0,0,0]
    cur_amounts_new = [0,0,0]
    cur_amounts_end = [0,0,0]
    for i in range(widget.rowCount()):
        cur_amounts_old[i] = float(widget.item(i,0).text())
    widget.add_spending(amount_add)
    for i in range(widget.rowCount()):
        cur_amounts_new[i] = float(widget.item(i,0).text())
    widget.delete_spending(amount_del)
    for i in range(widget.rowCount()):
        cur_amounts_end[i] = float(widget.item(i,0).text())
    assert all(cur_amounts_new[i] == cur_amounts_old[i] + float(amount_add) for i in range(3))
    assert all(cur_amounts_end[i] == cur_amounts_new[i] - float(amount_del) for i in range(3))
    
def test_redact_budget(qtbot):
    widget = BudgetTable()
    qtbot.addWidget(widget)
    
    assert all(widget.item(i, 1).text() == str(0) for i in range(3))  
    assert all(widget.item(i, 0).text() == str(0) for i in range(3))
    
    budgets = [300, 700, 1300]
    widget.fill_numbers(*budgets)
    
    assert all(widget.item(i, 1).text() == str(budgets[i]) for i in range(3)) 
    
    
def test_add_cat(qtbot):
    widget = CatChoice()
    qtbot.addWidget(widget)
    list_names = ["Животные", "Машины", "Поездки"]
    widget.set_cats_list(list_names)
    assert all(widget.itemText(i) == list_names[i] for i in range(widget.count()))
    
    name = "Кино"
    widget.add_item(name)
    assert widget.itemText(widget.count() - 1) == name
    
    

def test_main_window_cats(qtbot):
    widget = MyMainWindow()
    qtbot.addWidget(widget)
    cat_field = widget.red_field.combobox
    
    items = ["продукты", "молоко", "корм"]
    widget.set_categories(items)
    cnt_beg = cat_field.count()
    all_cats = [cat_field.itemText(i) for i in range(cnt_beg)]
    assert all_cats == items
    
    
    name = "Тестовая категория"
    widget.add_category(name)
    cnt = cat_field.count()
    assert cat_field.itemText(cnt - 1) == name
    
    cnt_new = cat_field.count()
    all_items = [cat_field.itemText(i) for i in range(cnt_new)]
    cats = cat_field.get_cats()
    assert cats == all_items
    
 
def test_cancel_expense(qtbot):
    widget = MyMainWindow()
    qtbot.addWidget(widget)
    data = data_for_testing()
    widget.fill_table_data(data)
    
    
    rows_before = widget.table.rowCount()
    spents_before = float(widget.budget_table.item(0,0).text())
    num_rows = widget.table.rowCount()
    amount = float(widget.table.item(num_rows - 1, 1).text())
    
    qtbot.mouseClick(
        widget.red_field.delbut,
        qt_api.QtCore.Qt.MouseButton.LeftButton
        )
    
    spents_after = float(widget.budget_table.item(0,0).text())
    rows_after = widget.table.rowCount()
    assert rows_after == rows_before - 1
    assert spents_after == spents_before - amount
    
    

    
    
    
    
    
    
    
    
    

