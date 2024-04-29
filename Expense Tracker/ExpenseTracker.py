import flet
from flet import *
import datetime
import database
import graphs
from copy import deepcopy
#FEEL FREE TO CHANGE COLOURS

#insert[-1] in show_ananlysis functions
#disconnect textfields and dropdowns of add page and edit page
# duplicate category throught edit
#all of the categories cannot be deleted
#clear dropdowns when changed route

weekno=database.get_week_no(datetime.datetime.now().strftime("%d %m %Y"))

def main(page:Page):
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'
    PINK = '#eb06ff'
    CG='#201D1D'

    color_options = [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF',
        '#FFA500', '#800080', '#008000', '#800000', '#008080', '#808000',
        '#A52A2A', '#000080', '#808080', '#FFC0CB', '#800000', '#FF4500'
    ]

    color_names = [
        'Red', 'Green', 'Blue', 'Yellow', 'Cyan', 'Magenta',
        'Orange', 'Purple', 'Dark Green', 'Maroon', 'Teal', 'Olive',
        'Brown', 'Navy', 'Grey', 'Pink', 'Maroon', 'Orange Red'
    ]

    dropdown_options = [
            dropdown.Option(color_options[i], color_names[i]) for i in range(len(color_options))
        ]

    category_input = TextField(hint_text='Max 10 char',label="Enter new category!",color=colors.GREEN_600, expand=True, on_submit=lambda _:add_category())
    category_color_dropdown = Dropdown(
        width=125,
        options=dropdown_options,
        color=colors.GREEN_600,
        bgcolor=colors.GREY_900,
        )
    
    
    #initializing category names and colors
    category_list,category_colors=tuple(zip(*database.show_all_categories()))
    category_list=list(category_list)
    category_colors=list(category_colors)

#drop down for editdata page
    categoris_dropdown=Dropdown(
        width=125,
        options=[dropdown.Option(category_list[i]) for i in range(len(category_list))],
        color=colors.GREEN_600,
        bgcolor=colors.GREY_900,
        # on_change=lambda _: print(categoris_dropdown.value)
        )
    
    analysis_dropdown=Dropdown(
        width=100,
        options=[dropdown.Option("Day"),dropdown.Option("Week"),dropdown.Option("Month")],
        on_change=lambda _ : change_analysis_format(),#color=textlist[0],
        color=colors.GREEN_600,
        bgcolor=colors.GREY_900,
    )   

   #text field for EditData page
    Input_Amount=TextField(label="Enter Amount", expand=True, on_submit=lambda _:add_expense(),color=colors.GREEN_600)
    #text field for AddData page
    Input_Amount1=TextField(label="Enter Amount", expand=True, on_submit=lambda _:add_expense1(),color=colors.GREEN_600)
    #text field for login page
    Input_username=TextField(label="Enter Username",on_submit=lambda _:username_submit(),color=colors.WHITE)

    editdata_list=ListView(
        controls=[
            #list of containers displaying expense entries will be appended here
        ]
    )

    date=datetime.datetime.now().strftime("%d %m %Y")
    month=date[3:5]
#####################################################################################################################
# initializing pages
    category_container = ListView(
        expand=True,
        spacing=10,
        padding=10,
        # auto_scroll=True,
        controls=[]
    )
    dialog= None
#####################################################################################################################
#initializing some functions 
    def isleapyear(y:int):
        if y%400==0 or (y%4==0 and y%100!=0):
            return True
        else: return False

    def get_week_dates(week):
        #return end dates of week in string format
        date1=datetime.datetime(23,12,31)
        for i in range(week):
            date1=date1+datetime.timedelta(7)
        date2=date1+datetime.timedelta(6)
        date1,date2=date1.strftime("%d/%m/%Y"),date2.strftime("%d/%m/%Y")
        daterange=date1+' - '+date2
        return daterange
#####################################################################################################################
    # Home_Page_Contents.controls[0].content.controls=graphs.home_piechart(date)
    Home_Page_Contents=Row(                                                         #DAILY GRAPHS WILL APPEAR IN HOME PAGE
        controls=[Container(expand=True,
                        bgcolor = colors.GREY_900,
                        padding=padding.only(top=10,left=20,
                                right=20,bottom=5),
                                content=ListView(
                                    padding=0,
                                    controls=graphs.home_piechart(date)
                                )
                                        )
                                    ]
                                )

    Analysis_Daily_Contents=Row(
            controls=[Container(expand=True,
                                bgcolor=colors.GREY_900,
                                padding=padding.only(top=10,left=20,right=20,bottom=5),
                                content=ListView(auto_scroll=False,controls=[
                                                Row(
                                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                    controls=[
                                                        analysis_dropdown,

                                                    ]
                                                ),

                                                #daily
                                                Row(#date picker
                                                    alignment=MainAxisAlignment.CENTER,
                                                    controls=[
                                                        Card(
                                                            width=210,
                                                            height=50,
                                                            color=colors.GREY_900,
                                                            content=(
                                                                Row(
                                                                    controls=[
                                                                        IconButton(
                                                                            width=30,
                                                                            content=Icon(icons.ARROW_BACK_IOS,color=colors.GREEN_600),
                                                                            on_click=lambda _ : previous_date(),
                                                                        ),
                                                                        TextButton(
                                                                            width=120,
                                                                            content=Text(datetime.datetime.now().strftime("%d %m %Y"),color=colors.WHITE),
                                                                            on_click=lambda _: date_picker1.pick_date(),
                                                                            # style=ButtonStyle(elevation=100,surface_tint_color="blue"),
                                                                        ),
                                                                        IconButton(
                                                                            width=30,
                                                                            content=Icon(icons.ARROW_FORWARD_IOS,color=colors.GREEN_600),
                                                                            on_click=lambda _ : next_date(),
                                                                        )
                                                                    ]
                                                                )
                                                            )
                                                        ),
                                                ]),

                                                Container(#graph here
                                                            padding=0,
                                                        ),

                                                Column(#analysis list
                                                    controls=[
                                                        #elements will be appended here
                                                        Container(height=100)
                                                    ]
                                                    
                                                )
                                            ]
                                        )
                            )
                ]
            )

    Analysis_Weekly_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=colors.GREY_900,
                            padding=padding.only(top=10,left=20,right=20,bottom=5),
                            content=ListView(auto_scroll=False,controls=[
                                            Row(
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    analysis_dropdown,

                                                ]
                                            ),

                                            #daily
                                            Row(#date picker
                                                alignment=MainAxisAlignment.CENTER,
                                                controls=[
                                                    Card(
                                                        # width=210,
                                                        height=50,
                                                        color=colors.GREY_900,
                                                        content=(
                                                            Row(
                                                                controls=[
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_BACK_IOS,color=colors.GREEN_600),
                                                                        on_click=lambda _ : previous_week(),
                                                                    ),

                                                                    Text(get_week_dates(weekno),color=colors.WHITE),

                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_FORWARD_IOS,color=colors.GREEN_600),
                                                                        on_click=lambda _ : next_week(),
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                            ]),

                                            Container(#graph
                                                    padding=0,
                                                    width=200,
                                                    height=400,

                                                    ),

                                            Column(#analysis list
                                                controls=[
                                                    #elements will be appended here
                                                ]
                                                
                                            )
                                        ]
                                    )
                        )
            ]
        )
    
    Analysis_Monthly_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=colors.GREY_900,
                            padding=padding.only(top=10,left=20,right=20,bottom=5),
                            content=ListView(auto_scroll=False,controls=[
                                            Row(
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    analysis_dropdown,

                                                ]
                                            ),

                                            #daily
                                            Row(#date picker
                                                alignment=MainAxisAlignment.CENTER,
                                                controls=[
                                                    Card(
                                                        width=210,
                                                        height=50,
                                                        color=colors.GREY_900,
                                                        content=(
                                                            Row(
                                                                controls=[
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_BACK_IOS,color=colors.GREEN_600),
                                                                        on_click=lambda _ : previous_month(),
                                                                    ),
                                                                    TextButton(
                                                                        width=120,
                                                                        content=Text("uselesstext",color=colors.WHITE),#Text((datetime.datetime.now().strftime("%m %Y"))),
                                                                        on_click=lambda _: page.show_bottom_sheet(CupertinoBottomSheet(CupertinoActionSheet(
                                                                            title=Text("Select month"),
                                                                            cancel=CupertinoActionSheetAction(
                                                                                content=Text("Done"),
                                                                                on_click=lambda _ : page.close_bottom_sheet()

                                                                            ),
                                                                            actions=[month_picker])))
                                                                        
                                                                    ),
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_FORWARD_IOS),
                                                                        on_click=lambda _ : next_month(),
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                            ]),

                                            Container(#graph
                                                    padding=0,
                                                    width=200,
                                                    height=400,

                                                    ),

                                            Column(#analysis list
                                                controls=[
                                                    #elements will be appended here
                                                ]
                                                
                                            )
                                        ]
                                    )
                        )
            ]
        )
    
    Analysis_Contents=deepcopy(Analysis_Daily_Contents)

    AddData_Contents=Row(                                                   #PARTH CODE FOR PLUS BUTTON IN HOME SCREEN
            controls=[Container(expand=True,
                        bgcolor=colors.GREY_900,
                        padding=padding.only(top=10, left=20,
                                            right=20, bottom=5),
                        content=Column(controls=[
                            Row(alignment=MainAxisAlignment.CENTER,
                                controls=[
                                Card(
                                    width=150,
                                    height=40,
                                    elevation=1,
                                    color=colors.GREY_900,
                                    content=Text(value=datetime.datetime.today().strftime('%d/%m/%Y'),color=colors.GREEN_500,text_align=TextAlign.CENTER,weight=FontWeight.BOLD,size=20),
                                )
                            ]
                            ),
                            Row(alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    categoris_dropdown,
                                    Input_Amount1
                                ]
                            )
                        ])
                        )
                ]
            )

    Category_contents=Row(                                                             #TANISHQ CODE + PARTH SQL CODE HERE
        controls=[Container(expand=True,
                        bgcolor=colors.GREY_900,
                        padding=padding.only(top=10,left=20,
                                right=20,bottom=5),
                                content=Column(controls=[
                               Row(
                                   controls=[category_color_dropdown, category_input]),
                               category_container,
                               
                           ]
                        )
                                        )
                                    ]
                                )
    
    EditData_Contents=Row(                                                        #PARTH CODE FOR EDIT DATA PAGE
        controls=[Container(expand=True,
                           bgcolor=colors.GREY_900,
                           padding=padding.only(top=10, left=20,
                                               right=20, bottom=5),
                           content=ListView(controls=[
                                Row(#date picker
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Card(
                                        width=210,
                                        height=50,
                                        color=colors.GREY_900,
                                        content=(
                                            Row(
                                                controls=[
                                                    IconButton(
                                                        width=30,
                                                        content=Icon(icons.ARROW_BACK_IOS),
                                                        on_click=lambda _ : previous_date_dp(),
                                                    ),
                                                    TextButton(
                                                        width=120,
                                                        content=Text(datetime.datetime.now().strftime("%d %m %Y"),color="white"),
                                                        on_click=lambda _: date_picker2.pick_date(),
                                                    ),
                                                    IconButton(
                                                        width=30,
                                                        content=Icon(icons.ARROW_FORWARD_IOS),
                                                        on_click=lambda _ : next_date_dp(),
                                                    )
                                                ]
                                            )
                                        )
                                    ),
                            ]),

                            Row(
                                controls=[
                                    categoris_dropdown,
                                    Input_Amount
                                ]
                            ),

                            Divider(color=colors.BLACK,height=10,thickness=2),

                            editdata_list,
                           ]
                           )
                           )
                  ]
              )


    About_us_contents = Container(expand=True,
        content=ListView(
            # horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Container(
                        expand=True,
                        bgcolor=colors.GREY_900,
                        content=Image(
                            src="iitpkd_logo3.png",
                            width=200,
                            height=200,
                            fit=ImageFit.CONTAIN
                        ),
                    ),
                Container(height=20),
                Container(
                    margin=padding.all(0),
                    content=Text(
                        "Group Members: ",
                        size=20,
                        color=colors.WHITE,
                        text_align='center'
                    ),
                ),
                Container(
                    margin=padding.all(0),
                    content=Text(
                        "Shelar Parth Vijay - 142301033",
                        size=20,
                        color=colors.WHITE,
                        text_align='center'
                    ),
                ),
                Container(
                    margin=padding.all(0),
                    content=Text(
                        "Shreesh Amit Chembeti - 132301032",
                        size=20,
                        color=colors.WHITE,
                        text_align='center'
                    ),
                ),
                Container(
                    margin=padding.all(0),
                    content=Text(
                        "Tanishq Chandra - 142301035",
                        size=20,
                        color=colors.WHITE,
                        text_align='center'
                    ),
                ),
                Divider(height=50,thickness=3,color=colors.GREY_500),

                Container(
                    padding=10,
                    content=Row(wrap=True,controls=[
                    Icon(name=icons.INFO_OUTLINE_ROUNDED,color=colors.GREY_400,size=15),
                    Text(
                        "This is an Android app named 'Expense Tracker' created by us for 'Introduction to Programming' course.\n -Project 2024",
                        size=17,
                        color=colors.GREY_400,
                    )
                    ])
                ),
                Container(height=30),
            ],
        )
        )



    
    
#####################################################################################################################

    def add_category():
        new_category = category_input.value[:10]
        new_color = category_color_dropdown.value
        if new_category and new_color:
            if new_category in category_list:
                show_duplicate_dialog(new_category)
            else:
                category_list.append(new_category)
                category_colors.append(new_color)
                add_category_row(new_category, new_color)
                database.insert_category(new_category,new_color)
                category_input.value = ""
                category_color_dropdown.value = None
                # category_input.on_submit =lambda _: add_category()  # Reset the on_submit function lookupagain
                update_dropdown()
                page.update()

    def show_duplicate_dialog(category):
        global dialog
        dialog = AlertDialog(
            title=Text("Duplicate Category"),
            content=Text(f"The category '{category}' has already been used."),
            actions=[
                IconButton(on_click=lambda _: close_dialog(), icon=icons.CLOSE_ROUNDED, 
#                           alignment=alignment.top_right
                           )
            ],
            on_dismiss=lambda e: print("Dialog dismissed!"),
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_dialog():
        global dialog
        dialog.open = False
        page.update()

    def add_category_row(category, color):
        category_container.controls.insert(-1,Container(bgcolor=colors.TRANSPARENT, border_radius=15, padding=5, content=
            Row(
                alignment='spaceBetween',
                controls=[
                    Container(
                        width=20,
                        height=20,
                        bgcolor=color,
                        border_radius=10,
                        margin=margin.only(right=10)
                    ),

                    Text(category, color="white",size=20),
                    Row(
                        controls=[
                            IconButton(
                                content=Icon(icons.EDIT),
                                on_click=lambda _: edit_category(category)
                            ),
                            IconButton(
                                content=Icon(icons.DELETE_FOREVER),
                                on_click=lambda _: delete_category(category)
                            )
                        ]
                    )
                ]
            )
        ))
        page.update()

    def edit_category(category):
        category_index = category_list.index(category)
        category_input.value = category_list[category_index]
        category_color_dropdown.value = category_colors[category_index]
        # if category_input.value and category_color_dropdown.value:
        #     if category_input.value in category_list:
        #         show_duplicate2_dialog(category_input.value)

        def update_category(e):
            new_category = category_input.value[:10]
            new_color = category_color_dropdown.value

            if new_color in color_options:
                new_color_index = color_options.index(new_color)
                if new_category in category_list:
                    show_duplicate_dialog(new_category)
                else:
                    # Only update category name if it's not a duplicate
                    old_data = (category_list[category_index], category_colors[category_index]) 
                    category_list[category_index] = new_category
                    category_colors[category_index] = color_options[new_color_index]
                    new_data = (category_list[category_index], category_colors[category_index])
                    database.edit_category(old_data, new_data) #update db file through sqlite3
                    update_dropdown()
                    # Rebuild the entire category container
                    rebuild_category_container()

            category_input.value = ""
            category_color_dropdown.value = None
            category_input.on_submit = add_category  # Reset the on_submit function
            page.update()
        category_input.on_submit = update_category
        category_input.focus()  # Set focus to the text field
        page.update()

    def edit_expense(category,amount,date):
        EditData_Contents.controls[0].content.controls[1].controls[0].value=category
        Input_Amount.value=amount
        def update_expense():
            new_category=EditData_Contents.controls[0].content.controls[1].controls[0].value
            new_amount=Input_Amount.value
            # database.edit_expense((category,amount,date),(new_category,new_amount,date))
            # build_editdata()
            # Input_Amount.value=None
            # Input_Amount.on_submit=lambda _:add_expense()
            # EditData_Contents.controls[0].content.controls[1].controls[0].value=None
            # page.update()
                # date=EditData_Contents.controls[0].content.controls[0].controls[0].content.controls[1].content.value
            try:
                new_amount=float(new_amount)
                if new_amount<=0:
                    open_error_snackbar()
                    return 
                database.edit_expense((category,amount,date),(new_category,new_amount,date))#database.insert_expense((category,amount,date))
                build_editdata()#add_editdata_row(database.get_category_color(category),category,amount,date)
                open_snackbar_addedexpense()
            except Exception as exp:
                print("exception",exp)
                open_error_snackbar()
            finally:
                #reset the dropdown and texfield
                Input_Amount.value=None
                Input_Amount.on_submit=lambda _:add_expense()
                EditData_Contents.controls[0].content.controls[1].controls[0].value=None
                page.update()
        Input_Amount.on_submit=lambda _: update_expense()
        Input_Amount.focus()
        page.update()

    def delete_category(category):
        if len(category_list)==1:
            show_last_category_dialog(category)
        else:
            category_index = category_list.index(category)
            def confirm_delete(choice):
                if choice == 'yes':
                    x=category_list.pop(category_index)
                    y=category_colors.pop(category_index)
                    database.delete_category(x,y)
                    update_dropdown()
                    # Remove the corresponding controls from the category_container
                    for index, control in enumerate(category_container.controls):
                        if isinstance(control, Container) and control.content.controls[1].value == category:
                            category_container.controls.pop(index)
                            break
                dialog.open = False  # Hide the dialog box after clicking "Yes" or "No"

                page.update()

            dialog = AlertDialog(
                title=Text("Delete Category"),
                content=Text(f"Are you sure you want to delete the category '{category}'?"),
                actions=[
                    TextButton("No", on_click=lambda _: (confirm_delete('no'))),
                    TextButton("Yes", on_click=lambda _: (confirm_delete('yes')))
                ],
                on_dismiss=lambda e: print("Dialog dismissed!"),
            )

            page.dialog = dialog
            dialog.open = True
            page.update()

    def show_last_category_dialog(category):
            global dialog
            dialog = AlertDialog(
                title=Text("Only Category"),
                content=Text(f"You cannot delete '{category}' as it is the only category remaining!"),
                actions=[
                    IconButton(on_click=lambda _: close_dialog(), icon=icons.CLOSE_ROUNDED, 
    #                           alignment=alignment.top_right
                            )
                ],
                on_dismiss=lambda e: print("Dialog dismissed!"),
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
    
    def rebuild_category_container():
        category_container.controls.clear()
        category_container.controls.append(Container(height=30))
        for category, color in zip(category_list, category_colors):
            add_category_row(category, color)


    def add_expense():
        category=EditData_Contents.controls[0].content.controls[1].controls[0].value
        amount=Input_Amount.value
        try:
            amount=float(amount)
            if amount<=0:
                open_error_snackbar()
                return 
            date=EditData_Contents.controls[0].content.controls[0].controls[0].content.controls[1].content.value
            database.insert_expense((category,amount,date))
            add_editdata_row(database.get_category_color(category),category,amount,date)
            open_snackbar_addedexpense()
        except Exception as exp:
            print("exception",exp)
            open_error_snackbar()
        finally:
            #reset the dropdown and texfield
            EditData_Contents.controls[0].content.controls[1].controls[0].value=None
            Input_Amount.value=None
            page.update()
    
    def add_expense1():
        category=AddData_Contents.controls[0].content.controls[1].controls[0].value
        amount=Input_Amount1.value
        try:
            amount=float(amount)
            if amount<=0:
                open_error_snackbar()
                return 
            date=datetime.datetime.today().strftime("%d %m %Y")
            database.insert_expense((category,amount,date))
            open_snackbar_addedexpense()
        except Exception as exp:
            print("exception",exp)
            open_error_snackbar()
        finally:
            Input_Amount1.value=None
            AddData_Contents.controls[0].content.controls[1].controls[0].value=None
            page.update()

    def open_error_snackbar():
        page.snack_bar=SnackBar(content=Text("Incorrect data type entered! Enter a positive real number"),duration=3000,behavior=SnackBarBehavior.FLOATING,show_close_icon=True)
        page.snack_bar.open=True
    def open_snackbar_addedexpense():
        page.snack_bar=SnackBar(content=Text("Expense Added Successfully!"),duration=3000,
                               behavior=SnackBarBehavior.FLOATING,show_close_icon=True)
        page.snack_bar.open=True


    def add_editdata_row(category_color,category,amount,date):
            editdata_list.controls.append(
                Row(
                alignment='spaceBetween',
                controls=[
                    Container(
                        width=20,
                        height=20,
                        bgcolor=category_color,
                        border_radius=10,
                        margin=margin.only(right=10)
                    ),

                    Text(category, color=colors.WHITE,size=20),
                    Text(amount, color=colors.WHITE,size=20),
                    Row(
                        controls=[
                            IconButton(
                                content=Icon(icons.EDIT),
                                on_click=lambda _: edit_expense(category,amount,date)
                            ),
                            IconButton(
                                content=Icon(icons.DELETE_FOREVER),
                                on_click=lambda _: delete_expense(category,amount,date)
                            )
                        ]
                    )
                ]
            )
            )

    def build_editdata():
        editdata_list.controls.clear()
        present_date=EditData_Contents.controls[0].content.controls[0].controls[0].content.controls[1].content.value
        data_list=database.show_daily_expense(present_date)
        for cat,clr,amt,c,d in data_list:
            add_editdata_row(clr,cat,amt,present_date)
        editdata_list.controls.append(Container(height=40))

    def update_dropdown():
        new_dropdown=Dropdown(
        width=175,
        options=[dropdown.Option(category_list[i]) for i in range(len(category_list))],
        # on_change=lambda _: print(new_dropdown.value)
        color=colors.GREEN_600,
        bgcolor=colors.GREY_900,
        )
        AddData_Contents.controls[0].content.controls[1].controls[0]=new_dropdown
        EditData_Contents.controls[0].content.controls[1].controls[0]=new_dropdown
        page.update()
    
    
    def delete_expense(category,amount,date):
        database.delete_expense((category,amount,date))
        build_editdata()
        page.update()

    def change_date1(e):
        # page.views[-1].controls[0].content.controls[1].controls[0].content.controls[1].content.value=Text(date_picker.value.strftime("%d %m %y"))
        Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=(date_picker1.value.strftime("%d %m %Y"))
        date=date_picker1.value.strftime("%d %m %Y")
        show_daily_analysis(date)
        
        # build_editdata()
        page.update()
    date_picker1 = DatePicker(
        on_change=change_date1,
        on_dismiss=lambda _:print("dismissed"),
        first_date=datetime.datetime(2024,1,1),
        current_date=datetime.datetime.today(),
        last_date=datetime.datetime.today(),

    )
    def change_date2(e):
        # page.views[-1].controls[0].content.controls[1].controls[0].content.controls[1].content.value=Text(date_picker.value.strftime("%d %m %y"))
        EditData_Contents.controls[0].content.controls[0].controls[0].content.controls[1].content.value=(date_picker2.value.strftime("%d %m %Y"))
        date=date_picker2.value.strftime("%d %m %Y")
        # show_daily_analysis(date)
        build_editdata()
        page.update()
    date_picker2 = DatePicker(
        on_change=change_date2,
        on_dismiss=lambda _:print("dismissed"),
        first_date=datetime.datetime(2024,1,1),
        current_date=datetime.datetime.today(),
        last_date=datetime.datetime.today(),

    )

    month_picker=CupertinoDatePicker(
        date_picker_mode=CupertinoDatePickerMode.MONTH_YEAR,
        on_change=lambda _ : change_month(),#print(month_picker.value.strftime("%m %Y"))
        last_date=datetime.datetime.today(),
        height=150
    )

    def change_month():
        Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=month_picker.value.strftime("%m %Y")
        show_monthly_analysis(month_picker.value.strftime("%m %Y"))
        page.update()

    def show_daily_analysis(date):
        Analysis_Contents.controls[0].content.controls[2].content=graphs.daily_piechart(date)
        Analysis_Contents.controls[0].content.controls[3].controls.clear()
        Analysis_Contents.controls[0].content.controls[3].controls.append(Row(controls=[Text(value="\n* Total expense is "+ (str(database.sumofday(date)) if database.sumofday(date)!=False else "0.0"),weight=FontWeight.NORMAL,color=colors.LIGHT_GREEN,size=20)]))
        Analysis_Contents.controls[0].content.controls[3].controls.append(
            Row(
                controls=[
                    Container(
                        expand=True,
                        height=50,
                        padding=padding.only(top=20),
                        # color=FG,
                        content=(
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Text("  categories",italic=True,color=colors.GREEN_600,size=20,),
                                    Text("amount    ",italic=True,color=colors.GREEN_600,size=20,)
                                ]
                            )
                        )
                    )
                ]
            )
        )

        # Analysis_Contents.controls[0].content.controls[3].controls.append(Container(expand=True,height=40,content=Row(expand=True,controls=[Text(value="Total expense is "+ str(database.sumofday(date)),weight=FontWeight.BOLD,color=colors.RED_ACCENT)])))
        Analysis_Contents.controls[0].content.controls[3].controls.append(Divider(thickness=3,color=colors.GREEN_900))

        cat_dict=database.show_categorywise_daily_expense(date)

        for cat in cat_dict:
               Analysis_Contents.controls[0].content.controls[3].controls.append(
                    Row(
                                                                controls=[
                                                                    Container(
                                                                        expand=True,
                                                                        height=30,
                                                                        bgcolor=colors.TRANSPARENT,
                                                                        content=(
                                                                            Row(
                                                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                                controls=[
                                                                                    #cate color, cate name, amount
                                                                                    Text("    "+cat,color=cat_dict[cat][1],size=20),
                                                                                    Text(str(cat_dict[cat][0]) + "    ",color=cat_dict[cat][1],size=20)
                                                                                    
                                                                                ]
                                                                            )
                                                                        ),
                                                                    ),
                                                                    
                                                                ]
                                                                
                                                            ),
                )
        Analysis_Contents.controls[0].content.controls[3].controls.append(Container(height=30))
        page.update()

    def show_weekly_analysis(week):
        #week is week number
        Analysis_Contents.controls[0].content.controls[2].content=graphs.weekly_linechart(week)
        Analysis_Contents.controls[0].content.controls[3].controls.clear()
        Analysis_Contents.controls[0].content.controls[3].controls.append(Row(controls=[Text(value="\n* Total expense is "+ (str(database.sumofweek(week))),weight=FontWeight.NORMAL,color=colors.LIGHT_GREEN,size=20)]))

        Analysis_Contents.controls[0].content.controls[3].controls.append(
            Row(
                controls=[
                    Container(
                        expand=True,
                        height=50,
                        padding=padding.only(top=20),
                        #color=colors.GREEN_600,
                        content=(
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Text("  categories",italic=True,color=colors.GREEN_600,size=20),
                                    Text("amount    ",italic=True,color=colors.GREEN_600,size=20)
                                ]
                            )
                        )
                    )
                ]
            )
        )
        Analysis_Contents.controls[0].content.controls[3].controls.append(Divider(thickness=3,color=colors.GREEN_900))
        cat_dict=database.show_weekly_expense(week)
        for cat in cat_dict:
            Analysis_Contents.controls[0].content.controls[3].controls.append(
                    Row(
                                                                controls=[
                                                                    Container(
                                                                        expand=True,
                                                                        height=30,
                                                                        bgcolor=colors.TRANSPARENT,
                                                                        content=(
                                                                            Row(
                                                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                                controls=[
                                                                                    #cate color, cate name, amount
                                                                                    Text("    "+cat,color=cat_dict[cat][1],size=20),
                                                                                    Text(str(cat_dict[cat][0]) + "    ",color=cat_dict[cat][1],size=20)
                                                                                    
                                                                                ]
                                                                            )
                                                                        ),
                                                                    ),
                                                                    
                                                                ]
                                                                
                                                            ),
                )
        Analysis_Contents.controls[0].content.controls[3].controls.append(Container(height=30))

    def show_monthly_analysis(month):
        #month is "mm yyyy"
        Analysis_Contents.controls[0].content.controls[2].content=graphs.monthly_linechart(month)
        Analysis_Contents.controls[0].content.controls[3].controls.clear()
        Analysis_Contents.controls[0].content.controls[3].controls.append(Row(controls=[Text(value="\n* Total expense is "+ (str(database.sumofmonth(month))),weight=FontWeight.NORMAL,color=colors.LIGHT_GREEN,size=20)]))
        Analysis_Contents.controls[0].content.controls[3].controls.append(
            Row(
                controls=[
                    Container(
                        expand=True,
                        height=50,
                        padding=padding.only(top=20),
                        # color=FG,
                        content=(
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Text("  categories",italic=True,size=20,color=colors.GREEN_600),
                                    Text("amount    ",italic=True,size=20,color=colors.GREEN_600)
                                ]
                            )
                        )
                    )
                ]
            )
        )
        Analysis_Contents.controls[0].content.controls[3].controls.append(Divider(thickness=3,color=colors.GREEN_900))
        cat_dict=database.show_monthly_expense(month)
        for cat in cat_dict:
            Analysis_Contents.controls[0].content.controls[3].controls.append(
                    Row(
                                                                controls=[
                                                                    Container(
                                                                        expand=True,
                                                                        height=30,
                                                                        bgcolor=colors.TRANSPARENT,
                                                                        content=(
                                                                            Row(
                                                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                                controls=[
                                                                                    #cate color, cate name, amount
                                                                                    Text("    "+cat,color=cat_dict[cat][1],size=20),
                                                                                    Text(str(cat_dict[cat][0]) + "    ",color=cat_dict[cat][1],size=20)
                                                                                    
                                                                                ]
                                                                            )
                                                                        ),
                                                                    ),
                                                                    
                                                                ]
                                                                
                                                            ),
                )
        Analysis_Contents.controls[0].content.controls[3].controls.append(Container(height=30))

    def change_analysis_format():
        if analysis_dropdown.value=="Day":
            Analysis_Contents.controls[0]=Analysis_Daily_Contents.controls[0]
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=datetime.datetime.now().strftime("%d %m %Y")
            show_daily_analysis(datetime.datetime.now().strftime("%d %m %Y"))
        if analysis_dropdown.value=="Week":
            Analysis_Contents.controls[0]=Analysis_Weekly_Contents.controls[0]
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].value=get_week_dates(database.get_week_no(datetime.datetime.now().strftime("%d %m %Y")))
            show_weekly_analysis(database.get_week_no(datetime.datetime.now().strftime("%d %m %Y")))

        if analysis_dropdown.value=="Month":
            Analysis_Contents.controls[0]=Analysis_Monthly_Contents.controls[0]
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=datetime.datetime.now().strftime("%m %Y")
            show_monthly_analysis(datetime.datetime.now().strftime("%m %Y"))
        page.update()

    def previous_date_dp():
        presentday_str='-'.join(list((EditData_Contents.controls[0].content.controls[0].controls[0].content.controls[1].content.value).split())[::-1])
        presentday=datetime.datetime.fromisoformat(presentday_str)
        yesterday = presentday - datetime.timedelta(1)
        EditData_Contents.controls[0].content.controls[0].controls[0].content.controls[1].content.value=yesterday.strftime('%d %m %Y')
        date=yesterday.strftime('%d %m %Y')
        build_editdata()
        page.update()

    def next_date_dp():
        presentday_str='-'.join(list((EditData_Contents.controls[0].content.controls[0].controls[0].content.controls[1].content.value).split())[::-1])
        presentday=datetime.datetime.fromisoformat(presentday_str)
        tomorrow = presentday + datetime.timedelta(1)
        if tomorrow>datetime.datetime.today():
            pass
        else:
            EditData_Contents.controls[0].content.controls[0].controls[0].content.controls[1].content.value=tomorrow.strftime('%d %m %Y')
            date=tomorrow.strftime('%d %m %Y')
            build_editdata()
            page.update()

    def previous_date():
        presentday_str='-'.join(list((Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value).split())[::-1])
        presentday=datetime.datetime.fromisoformat(presentday_str)
        yesterday = presentday - datetime.timedelta(1)
        Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=yesterday.strftime('%d %m %Y')
        date=yesterday.strftime('%d %m %Y')
        show_daily_analysis(date)
        page.update()
    
    def next_date():

        presentday_str='-'.join(list((Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value).split())[::-1])
        presentday=datetime.datetime.fromisoformat(presentday_str)
        tomorrow = presentday + datetime.timedelta(1)
        if tomorrow>datetime.datetime.today():
            pass
        else:
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=tomorrow.strftime('%d %m %Y')
            date=tomorrow.strftime('%d %m %Y')
            show_daily_analysis(date)
            page.update()

    def previous_week():
        global weekno
        prvweek=weekno-1
        if (prvweek)>=0:
            weekno=prvweek
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].value=get_week_dates(prvweek)
            show_weekly_analysis(prvweek)
        page.update()

    def next_week():
        global weekno
        nextweek=weekno+1
        if database.get_week_no(datetime.datetime.now().strftime("%d %m %Y"))>=nextweek>=0:
            weekno=nextweek 
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].value=get_week_dates(nextweek)
            show_weekly_analysis(nextweek)
        page.update()

    def previous_month():
        presentmonth_str='01 '+Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value #or month_picker.value
        presentmonth_str="-".join(presentmonth_str.split()[::-1])
        # print(presentmonth_str)
        present_month=datetime.datetime.fromisoformat(presentmonth_str)
        prvmonth=present_month-datetime.timedelta(1)
        prvmonth_str=prvmonth.strftime("%m %Y")
        Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=prvmonth_str
        show_monthly_analysis(prvmonth_str)
        page.update()
    
    def next_month():
        mmyyyy=Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value #or month_picker.value
        if int(mmyyyy[:2]) in [1,3,5,7,8,10,12]:
            presentmonth_str='31 '+mmyyyy
        elif int(mmyyyy[:2]) in [4,6,9,11]:
            presentmonth_str='30 '+mmyyyy
        else:
            if isleapyear(int(mmyyyy[3:])):
                presentmonth_str='29 '+mmyyyy
            else:
                presentmonth_str='28 '+mmyyyy
        presentmonth_str="-".join(presentmonth_str.split()[::-1])
        # print(presentmonth_str)
        present_month=datetime.datetime.fromisoformat(presentmonth_str)
        nxtmonth=present_month+datetime.timedelta(1)
        if nxtmonth<=datetime.datetime.today():
            nxtmonth_str=nxtmonth.strftime("%m %Y")
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=nxtmonth_str
            show_monthly_analysis(nxtmonth_str)
        else:   
            #enter dialog here
            pass
        page.update()
    

#####################################################################################################################
    
    Home_Page= Container(expand=True,visible=True,content=Home_Page_Contents)

    Analysis_Page = Container(expand=True,visible=False,content=Analysis_Contents)

    Category_Page = Container(expand=True,visible=False,content=Category_contents)

    EditData_Page = Container(expand=True,
                          visible=False,
                          content=EditData_Contents)

    Initial_Page=Container(expand=True,
                           content=Row(
                               [
                                    Home_Page,
                                    Analysis_Page,
                                    Category_Page,
                                    EditData_Page,
                                    ]
                                )
                            )
    


#####################################################################################################################

    pages={'/':View('/',[Initial_Page],floating_action_button = FloatingActionButton(icon=icons.ADD_OUTLINED,
                                        bgcolor=colors.GREEN_600,
                                        #foreground_color=colors.BLACK,
                                        shape=CircleBorder(),
                                        width=50,
                                        on_click=lambda _:page.go('/AddData_Contents')),
               floating_action_button_location = FloatingActionButtonLocation.CENTER_DOCKED,

                appbar=AppBar(automatically_imply_leading=False,bgcolor=CG,title=Text(value='ExpenseTracker',size=20,color='white',italic=True,weight=FontWeight.BOLD),actions=[IconButton(icon=icons.MENU,on_click=lambda e:show_drawer(e))]),

                end_drawer = NavigationDrawer(selected_index=-1,
                                              bgcolor=colors.BLACK87,
                                              on_change=lambda e:changedrawertab(e),
                                                controls=[
                                                Divider(thickness=2,color=colors.WHITE12),
                                                Text(value="",color=colors.WHITE,text_align='center'),  #username
                                                Divider(thickness=2,color=colors.WHITE12),
                                                NavigationDrawerDestination(
                                                        label="About us",
                                                        icon=icons.INFO_OUTLINE,
                                                        )
                                                        ]
                ),


                bottom_appbar = NavigationBar(
                        bgcolor=CG,
                        selected_index=0,
                        on_change=lambda e:changetab(e),
                        destinations=[
                        NavigationDestination(label='Home',icon=icons.HOME_OUTLINED,selected_icon=icons.HOME),
                        NavigationDestination(label='Analysis',icon=icons.ANALYTICS_OUTLINED,selected_icon=icons.ANALYTICS),
                        NavigationDestination(label='Categories',icon=icons.CATEGORY_OUTLINED,selected_icon=icons.CATEGORY),
                        NavigationDestination(label='EditData',icon=icons.DATASET_OUTLINED,selected_icon=icons.DATASET),
                        ]
                         )
                ),
           '/AddData_Contents':View('/AddData_Contents',[Container(expand=True,
                                                 bgcolor=colors.GREEN_600,
                                                 content=AddData_Contents)],
                                        AppBar(leading=IconButton(icon=icons.ARROW_BACK,on_click=lambda _:go_back_tomainpage(),tooltip='Go back'),#on long press do nothing/dismiss
                                                bgcolor=CG,
                                                title=Text('Expense today',size=20))),                                            
            '/About_us':View('/About_us',[Container(
                expand=True,
                bgcolor=colors.GREY_900,
                content=About_us_contents)],
                AppBar(leading=IconButton(icon=icons.ARROW_BACK,on_click=lambda _:page.go("/"),tooltip='Go back'),#on long press do nothing/dismiss
                                          bgcolor=CG,
                                          title=Text(value='About us',size=20,weight=FontWeight.BOLD,italic=True))),
            '/Login':View('/Login',[
                Container(
                    padding=20,
                    bgcolor=colors.GREY_900,
                    expand=True,
                    animate=animation.Animation(600, AnimationCurve.DECELERATE),
                    content=Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Container(
                                padding=20,
                                bgcolor=colors.GREY_500,
                                border_radius=10,
                                content=Column(
                                    controls=[
                                        Text(
                                            value='Create your Account!',
                                            text_align='center',
                                            size=30,
                                            color=colors.WHITE,
                                            weight=FontWeight.BOLD,
                                        ),
                                        Input_username,
                                    ]
                                )
                            )
                        ]
                    )
                )
            ])
                }
    
    def go_back_tomainpage():
        page.go("/")
        page.update()

    def update_chart():
        Home_Page_Contents.controls[0].content.controls=graphs.home_piechart(date)


#####################################################################################################################
    def show_drawer(e):
        pages['/'].end_drawer.open = True
        page.update()
    # def show_end_drawer(e):
    #     page.views[0].show_end_drawer(end_drawer)
    def changetab(e):
        my_index = e.control.selected_index
        if my_index == 0:
            update_chart()
            Home_Page.visible = True 
            pages['/'].appbar.title.value='ExpenseTracker'

        else:
            Home_Page.visible=False


        if my_index == 1:
            change_analysis_format()
            Analysis_Page.visible = True
            pages['/'].appbar.title.value='Analysis'
            
        else :
            Analysis_Page.visible = False


        if my_index == 2:
            Category_Page.visible = True
            pages['/'].appbar.title.value='Categories'
        else :
            Category_Page.visible = False


        if my_index == 3:
            build_editdata()
            EditData_Page.visible = True
            pages['/'].appbar.title.value='Edit Data'
        else :
            EditData_Page.visible = False

        page.update()

    def changedrawertab(e):
        my_drawer_index = e.control.selected_index

        page.views[-1].end_drawer.selected_index=-1 #Return to original state

        if my_drawer_index==0:
            page.go('/About_us')
        
    def change_route(route):
        #clear dropdowns and textfields function?

        if page.route=='/':
            page.views.clear()
            page.views.append(View())
            page.views.append(
            pages['/']
            )
            update_chart()
            build_editdata()
            change_analysis_format()
            rebuild_category_container()



        else:
            page.views.clear()
            page.views.append(View())
            page.views.append(
                pages[page.route]
                )
            
        page.views[-1].padding=0 #permanently sets page padding to zero even when pages are changed
        page.update()


#####################################################################################################################

    def username_submit():
        database.submit_username(Input_username.value)
        page.views.clear()
        page.views.append(View())
        page.views.append(pages['/'])
        pages['/'].end_drawer.controls[1].value="Welcome "+database.get_username()+" !"
        page.views[-1].padding=0 
        build_editdata()
        show_daily_analysis(date)
        rebuild_category_container()

 

    if database.check_username():
        page.views.clear()
        page.views.append(pages['/Login'])
        page.views[-1].padding=0
        page.update()
        
    
    else:
        page.views.clear()
        page.views.append(View())
        page.views.append(pages['/'])
        pages['/'].end_drawer.controls[1].value="Welcome "+database.get_username()+" !"
        page.views[-1].padding=0 
        build_editdata()
        show_daily_analysis(date)
        rebuild_category_container()



    analysis_dropdown.value="Day"
    page.on_route_change= change_route 
    page.overlay.extend([date_picker1,date_picker2])
    page.theme=Theme(color_scheme_seed=colors.GREEN_600)
    page.update()

flet.app(target=main)