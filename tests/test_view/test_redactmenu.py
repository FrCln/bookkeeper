from pytestqt.qt_compat import qt_api
from bookkeeper.view.Redactclass import MainTable, BudgetTable, CatChoice, RedactField, MyMainWindow
from bookkeeper.view.redactmenu import RedactMenu, CommentMenu, AddMenu, DelMenu, BudgetMenu


def test_add_menu(qtbot):
    main_widget = MyMainWindow()
    redact_widget = RedactMenu(parent = main_widget)
    add_widget = AddMenu(parent = redact_widget)
    
    def ghost(cat1, cat2):
        return 0
        
    main_widget.register_cat_adder(ghost)
        
    qtbot.addWidget(main_widget)
    qtbot.addWidget(redact_widget)
    qtbot.addWidget(add_widget)
    
    len_before = add_widget.parent.parent.red_field.combobox.count()
    qtbot.mouseClick(
        add_widget.but,
        qt_api.QtCore.Qt.MouseButton.LeftButton
        )
        
    len_after = add_widget.parent.parent.red_field.combobox.count()
    assert len_after == len_before + 1
    
def test_del_menu(qtbot):
    main_widget = MyMainWindow()
    redact_widget = RedactMenu(parent = main_widget)
    del_widget = DelMenu(parent = redact_widget)
    name = "Продукты"
    main_widget.add_category(name)
    
    def ghost(cat1):
        return 0
        
    main_widget.register_cat_deleter(ghost)
    qtbot.addWidget(main_widget)
    qtbot.addWidget(redact_widget)
    qtbot.addWidget(del_widget)
    len_before = del_widget.parent.parent.red_field.combobox.count()
    
    qtbot.mouseClick(
        del_widget.but,
        qt_api.QtCore.Qt.MouseButton.LeftButton
        )
        
    len_after = del_widget.parent.parent.red_field.combobox.count()
    assert len_after == len_before - 1
    

def test_comm_menu(qtbot):
    main_widget = MyMainWindow()
    comm_widget = CommentMenu(parent = main_widget)
    qtbot.addWidget(main_widget)
    qtbot.addWidget(comm_widget)
    def ghost(cat1, cat2, cat3, cat4):
        return 0
        
    main_widget.register_expense_adder(ghost)
    rows_before = comm_widget.parent.table.rowCount()
    
    qtbot.mouseClick(
        comm_widget.but,
        qt_api.QtCore.Qt.MouseButton.LeftButton
        )
        
    rows_after = comm_widget.parent.table.rowCount()
    assert rows_after == rows_before + 1
    
    
    
    
    
    
    
    
