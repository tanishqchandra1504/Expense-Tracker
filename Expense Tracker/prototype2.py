import flet
from flet import *
import datetime
import database

def main(page:Page):
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'
    PINK = '#eb06ff'

    # conn=database.ConnectToDatabase()

    color_options = [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF',
        '#FFA500', '#800080', '#008000', '#800000', '#008080', '#808000',
        '#A52A2A', '#000080', '#808080', '#FFC0CB', '#800000', '#FF4500'
    ]

    color_names = [
        'Red', 'Green', 'Blue', 'Yellow', 'Cyan', 'Magenta',
        'Orange', 'Purple', 'Dark Green', 'Maroon', 'Teal', 'Olive',
        'Brown', 'Navy', 'Gray', 'Pink', 'Maroon', 'Orange Red'
    ]
    dropdown_options = [
            dropdown.Option(color_options[i], color_names[i]) for i in range(len(color_options))
        ]
    
    #initializing category names and colors
    category_list,category_colors=tuple(zip(*database.show_all_categories(database.ConnectToDatabase())))
    category_list=list(category_list)
    category_colors=list(category_colors)

    category_container = ListView(
        expand=True,
        spacing=10,
        padding=10,
        auto_scroll=True,
        controls=[]
    )
    #drop down for editdata page
    categories_dropdown1=Dropdown(
        width=125,
        options=[dropdown.Option(category_list[i]) for i in range(len(category_list))],
        on_change=lambda _: print(categories_dropdown1.value))
    
    page.padding=0
    date=datetime.datetime.now().strftime("%d %m %Y")
    month=date[3:5]


    #First page
    first_page_contents=Container(
        content=Column(
            controls=[Row(alignment='spaceBetween',
                        controls=[IconButton(on_click=lambda e:shrink(e),
                                            content=Icon(icons.ARROW_FORWARD)),
                                  IconButton(on_click=lambda _:page.go('/AddData'),
                                            content=Icon(icons.ADD))]
                                            )
                                        ]
                                    )
                                )

    page_1= Container(expand=True,
                bgcolor=BG,
                padding=20,
                content=Column(
                    controls=[Container(height=17),
                        IconButton(on_click=lambda e:restore(e),
                            content=Icon(icons.ARROW_BACK)),
                            Container(height=17),
                            Row(controls=[TextButton('Analysis',icon=icons.ANALYTICS_SHARP,on_click=lambda _:page.go('/Analysis'))]),
                            Container(height=17),
                            Row(controls=[TextButton('Categories',icons.CATEGORY_SHARP,on_click=lambda _:page.go('/Categories'))]),
                            Container(height=17),
                            Row(controls=[TextButton('Edit data',icon=icons.DATA_ARRAY_SHARP,on_click=lambda _:goto_editdata())]),
                            Container(height=17),
                            Row(controls=[TextButton('Settings',icon=icons.SETTINGS,on_click=lambda _:page.go('/Settings'))]),
                            Container(height=17),
                            Row(controls=[TextButton('Exit',icon=icons.EXIT_TO_APP_SHARP,on_click=lambda _:page.go('/Exit'))])

                            ]
                        )
                     )
    
    

    
    page_2= Row(alignment='end',#when animation happens it should move to right , default left  
        controls=[
            Container(expand=True,
                bgcolor=FG,
                animate=animation.Animation(600,AnimationCurve.DECELERATE),
                animate_scale=animation.Animation(400,AnimationCurve.DECELERATE),
                padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                content=Column(
                    controls=[
                        first_page_contents,
                        categories_dropdown1
                        ]
                    )
                )
            ]
        )

    container=Container(expand=True,
                         bgcolor=BG,
                        content=Stack(
                            controls=[
                            page_1,
                            page_2
                        ]
                    )
                )
    

    
    # Pop-up box
    dialog = None

    def add_category(e):
        new_category = category_input.value
        new_color = category_color_dropdown.value
        print(new_color)
        if new_category and new_color:
            if new_category in category_list:
                show_duplicate_dialog(new_category)
            else:
                category_list.append(new_category)
                category_colors.append(new_color)
                add_category_row(new_category, new_color)
                database.insert_category(database.ConnectToDatabase(),new_category,new_color)
                category_input.value = ""
                category_color_dropdown.value = None
                category_input.on_submit = add_category  # Reset the on_submit function
                Editdata_contents.controls[0].content.controls[2].controls[0]=update_dropdown()
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
        category_container.controls.append(Container(bgcolor=BG, border_radius=10, padding=15, content=
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

                    Text(category, color="white"),
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

        def update_category(e):
            new_category = category_input.value
            new_color = category_color_dropdown.value

            if new_color in color_options:
                new_color_index = color_options.index(new_color)
            else:
                new_color_index = int(new_color)
            old_data=(category_list[category_index],category_colors[category_index]) 
            category_list[category_index] = new_category
            category_colors[category_index] = color_options[new_color_index]
            new_data=(category_list[category_index],category_colors[category_index])
            database.edit_category(database.ConnectToDatabase(),old_data,new_data) #update db file through sqlite3
            Editdata_contents.controls[0].content.controls[2].controls[0]=update_dropdown()
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
        Editdata_contents.controls[0].content.controls[2].controls[0].value=category
        Input_Amount.value=amount
        def update_expense():
            new_category=Editdata_contents.controls[0].content.controls[2].controls[0].value
            new_amount=Input_Amount.value
            database.edit_expense(database.ConnectToDatabase(),(category,amount,date),(new_category,new_amount,date))
            build_editdata()

            Input_Amount.value=None
            Input_Amount.on_submit=lambda _:add_expense()
            Editdata_contents.controls[0].content.controls[2].controls[0].value=None
            page.update()
        Input_Amount.on_submit=lambda _: update_expense()
        Input_Amount.focus()
        page.update()

    def delete_category(category):
        category_index = category_list.index(category)

        def confirm_delete(choice):
            if choice == 'yes':
                x=category_list.pop(category_index)
                y=category_colors.pop(category_index)
                database.delete_category(database.ConnectToDatabase(),x,y)
                Editdata_contents.controls[0].content.controls[2].controls[0]=update_dropdown()
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
    
    def rebuild_category_container():
        category_container.controls.clear()
        for category, color in zip(category_list, category_colors):
            add_category_row(category, color)


    category_input = TextField(hint_text="Enter new category", expand=True, on_submit=add_category)
    category_color_dropdown = Dropdown(
        width=125,
        options=dropdown_options,
        on_change=lambda _: print(category_color_dropdown.value))
    
    Category_contents = Row(
        controls=[Container(expand=True,
                           bgcolor=FG,
                           padding=padding.only(top=50, left=20,
                                               right=20, bottom=5),
                           content=Column(controls=[
                               Row(
                                   controls=[IconButton(on_click=lambda _: page.go('/'),
                                                       content=Icon(icons.CLOSE_ROUNDED))]),
                               Row(
                                   controls=[category_color_dropdown, category_input]),
                               category_container
                           ]
                           )
                           )
                  ]
              )
    
    editdata_list=Column(
        controls=[

        ]
    )
    

    
    Input_Amount=TextField(hint_text="Enter amount", expand=False, on_submit=lambda _:add_expense())

    Editdata_contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                                     content=Column(controls=[
                                                    Row(
                                                    controls=[IconButton(on_click=lambda _:page.go('/'),
                                                    content=Icon(icons.CLOSE_ROUNDED))]),

                                                    Row(#date picker
                                                        alignment=MainAxisAlignment.CENTER,
                                                        controls=[
                                                            Card(
                                                                width=210,
                                                                height=50,
                                                                color=BG,
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
                                                                                content=Text(datetime.datetime.now().strftime("%d %m %Y")),
                                                                                on_click=lambda _: date_picker.pick_date(),
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
                                                            categories_dropdown1,
                                                            Input_Amount
                                                        ]
                                                    ),
                                                    Divider(color=BG,height=2),

                                                    editdata_list,
                                                    
                                                ]
                                            )
                                )
                            ]
                        )

    def add_expense():
        category=Editdata_contents.controls[0].content.controls[2].controls[0].value
        print(category)
        amount=Input_Amount.value
        date=Editdata_contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value
        database.insert_expense(database.ConnectToDatabase(),(category,amount,date))
        add_editdata_row(database.get_category_color(database.ConnectToDatabase(),category),category,amount,date)
        #reset the dropdown and texfield
        Editdata_contents.controls[0].content.controls[2].controls[0].value=None
        Input_Amount.value=None
        page.update()

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

                    Text(category, color="white"),
                    Text(amount, color = "black"),
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
        present_date=Editdata_contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value
        data_list=database.show_daily_expense(database.ConnectToDatabase(),present_date)
        for cat,amt,c,d in data_list:
            # print(cat,amt,database.get_category_color(database.ConnectToDatabase(),cat))
            add_editdata_row(database.get_category_color(database.ConnectToDatabase(),cat),cat,amt,present_date)

    def update_dropdown():
        new_dropdown=Dropdown(
        width=125,
        options=[dropdown.Option(category_list[i]) for i in range(len(category_list))],
        on_change=lambda _: print(new_dropdown.value))
        return new_dropdown
    
    
    def delete_expense(category,amount,date):
        database.delete_expense(database.ConnectToDatabase(),(category,amount,date))
        build_editdata()
        page.update()

    def goto_editdata():
        page.go('/Editdata')
        page.update()

    analysis_dropdown=Dropdown(
        width=100,
        options=[dropdown.Option("Day"),dropdown.Option("Week"),dropdown.Option("Month")],
        on_change=lambda _ : change_analysis_format(),
    )
    

    Analysis_Daily_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,right=20,bottom=5),
                            content=Column(controls=[
                                            Row(#close button
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    IconButton(
                                                        on_click=lambda _:page.go('/'),
                                                        content=Icon(icons.CLOSE_ROUNDED)
                                                        
                                                    ),
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
                                                        color=BG,
                                                        content=(
                                                            Row(
                                                                controls=[
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_BACK_IOS),
                                                                        on_click=lambda _ : previous_date(),
                                                                    ),
                                                                    TextButton(
                                                                        width=120,
                                                                        content=Text(datetime.datetime.now().strftime("%d %m %Y")),
                                                                        on_click=lambda _: date_picker.pick_date(),
                                                                        


                                                                    ),
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_FORWARD_IOS),
                                                                        on_click=lambda _ : next_date(),
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                            ]),

                                            Container(#graph
                                                        width=200,
                                                        height=200,

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
    
    Analysis_Weekly_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,right=20,bottom=5),
                            content=Column(controls=[
                                            Row(#close button
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    IconButton(
                                                        on_click=lambda _:page.go('/'),
                                                        content=Icon(icons.CLOSE_ROUNDED)
                                                        
                                                    ),
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
                                                        color=BG,
                                                        content=(
                                                            Row(
                                                                controls=[
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_BACK_IOS),
                                                                        on_click=lambda _ : previous_week(),
                                                                    ),
                                                                    TextButton(
                                                                        width=120,
                                                                        content=Text(database.get_week_no(datetime.datetime.now().strftime("%d %m %Y"))),
                                                                        on_click=lambda _: _#dropdown to select date,
                                                                    ),
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_FORWARD_IOS),
                                                                        on_click=lambda _ : next_week(),
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                            ]),

                                            Container(#graph
                                                        width=200,
                                                        height=200,

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
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,right=20,bottom=5),
                            content=Column(controls=[
                                            Row(#close button
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    IconButton(
                                                        on_click=lambda _:page.go('/'),
                                                        content=Icon(icons.CLOSE_ROUNDED)
                                                        
                                                    ),
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
                                                        color=BG,
                                                        content=(
                                                            Row(
                                                                controls=[
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_BACK_IOS),
                                                                        on_click=lambda _ : previous_month(),
                                                                    ),
                                                                    TextButton(
                                                                        width=120,
                                                                        content=Text(int(datetime.datetime.now().strftime("%m"))),
                                                                        on_click=lambda _:_#dropdown,
                                                                        


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
                                                        width=200,
                                                        height=200,

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


    Analysis_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,right=20,bottom=5),
                            content=Column(controls=[
                                            Row(#close button
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    IconButton(
                                                        on_click=lambda _:page.go('/'),
                                                        content=Icon(icons.CLOSE_ROUNDED)
                                                        
                                                    ),
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
                                                        color=BG,
                                                        content=(
                                                            Row(
                                                                controls=[
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_BACK_IOS),
                                                                        on_click=lambda _ : previous_date(),
                                                                    ),
                                                                    TextButton(
                                                                        width=120,
                                                                        content=Text(datetime.datetime.now().strftime("%d %m %Y")),
                                                                        on_click=lambda _: date_picker.pick_date(),
                                                                        


                                                                    ),
                                                                    IconButton(
                                                                        width=30,
                                                                        content=Icon(icons.ARROW_FORWARD_IOS),
                                                                        on_click=lambda _ : next_date(),
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                            ]),

                                            Container(#graph
                                                        width=200,
                                                        height=200,

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

    # Analysis_Contents=Analysis_Daily_Contents

    Settings_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                                     content=Column(controls=[
                                                    Row(
                                                    controls=[IconButton(on_click=lambda _:page.go('/'),
                                  content=Icon(icons.CLOSE_ROUNDED))])
                                        
                                        ]
                                    )
                                )
                            ]
                        )
    
    Exit_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                                     content=Column(controls=[
                                                    Row(
                                                    controls=[IconButton(on_click=lambda _:page.go('/'),
                                  content=Icon(icons.CLOSE_ROUNDED))])
                                        
                                        ]
                                    )
                                )
                            ]
                        )
    
    AddData_contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,
                                     right=20,bottom=5),
                                     content=Column(controls=[
                                                    Row(
                                                    controls=[IconButton(on_click=lambda _:page.go('/'),
                                  content=Icon(icons.CLOSE_ROUNDED))])
                                        
                                        ]
                                    )
                                )
                            ]
                        )
    
    #routing info
    pages={'/':View('/',[container]),
            '/Editdata':View('/Editdata',[Container(
                expand=True,
                bgcolor=FG,
                content=Editdata_contents
                                  
                )]),'/AddData':View('/AddData',[Container(
                expand=True,
                bgcolor=FG,
                content=AddData_contents
                                  
                )]),'/Analysis':View('/Analysis',[Container(
                expand=True,
                bgcolor=FG,
                content=Analysis_Contents
                                  
                )]),'/Categories':View('/Categories',[Container(
                expand=True,
                bgcolor=FG,
                content=Category_contents
                                  
                )]),
                
               
                '/Settings':View('/Settings',[Container(
                expand=True,
                bgcolor=FG,
                content=Settings_Contents
                
                )]),
                '/Exit':View('/Exit',[Container(
                expand=True,
                bgcolor=FG,
                content=Exit_Contents
                )])
    }

    #Route functions
    def shrink(e):
        page_2.controls[0].expand=False
        page_2.controls[0].width=page.width/2
        page_2.controls[0].scale=transform.Scale(0.8,alignment.center_right)
        page_2.controls[0].border_radius=25
        page_2.update()


    def restore(e):
        page_2.controls[0].width=page.width
        page_2.controls[0].scale=transform.Scale(1,alignment.center_right)
        page_2.controls[0].border_radius=None
        page_2.update()

    def change_route(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
        )
        page.views[-1].padding=0 #permanently sets page padding to zero even when pages are changed
        page.update()


    def show_daily_analysis(date):
        Analysis_Contents.controls[0].content.controls[3].controls.clear()
        Analysis_Contents.controls[0].content.controls[3].controls.append(
            Row(
                controls=[
                    Container(
                        expand=True,
                        height=50,
                        # color=FG,
                        content=(
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Text("  categories",italic=True),
                                    Text("amount    ",italic=True)
                                ]
                            )
                        )
                    )
                ]
            )
        )

        Analysis_Contents.controls[0].content.controls[3].controls.append(Divider(thickness=3,color="black"))
        for item in database.show_daily_expense(database.ConnectToDatabase(),date):
               Analysis_Contents.controls[0].content.controls[3].controls.append(
                    Row(
                                                                controls=[
                                                                    Card(
                                                                        expand=True,
                                                                        height=50,
                                                                        # border=border.all(0.85, "white54"),
                                                                        # border_radius=8,
                                                                        color=BG,
                                                                        content=(
                                                                            Row(
                                                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                                controls=[
                                                                                    #cate color, cate name, amount
                                                                                    Text("    "+item[0],color="white",size=30),
                                                                                    Text(str(item[1]) + "    ",color="white",size=30)
                                                                                    
                                                                                ]
                                                                            )
                                                                        ),
                                                                    ),
                                                                    
                                                                ]
                                                                
                                                            ),
                )


    def show_monthly_analysis(month):
        Analysis_Contents.controls[0].content.controls[3].controls.clear()
        Analysis_Contents.controls[0].content.controls[3].controls.append(
            Row(
                controls=[
                    Container(
                        expand=True,
                        height=50,
                        # color=FG,
                        content=(
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Text("  categories",italic=True),
                                    Text("amount    ",italic=True)
                                ]
                            )
                        )
                    )
                ]
            )
        )
        Analysis_Contents.controls[0].content.controls[3].controls.append(Divider(thickness=3,color="black"))
        for item in database.show_monthly_expense(database.ConnectToDatabase(),month):
            Analysis_Contents.controls[0].content.controls[3].controls.append(
                    Row(
                                                                controls=[
                                                                    Card(
                                                                        expand=True,
                                                                        height=50,
                                                                        # border=border.all(0.85, "white54"),
                                                                        # border_radius=8,
                                                                        color=BG,
                                                                        content=(
                                                                            Row(
                                                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                                controls=[
                                                                                    #cate color, cate name, amount
                                                                                    Text("    "+item[0],color="white",size=30),
                                                                                    Text(str(item[1]) + "    ",color="white",size=30)
                                                                                    
                                                                                ]
                                                                            )
                                                                        ),
                                                                    ),
                                                                    
                                                                ]
                                                                
                                                            ),
                )

    def previous_date_dp():
        presentday_str='-'.join(list((Editdata_contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value).split())[::-1])
        presentday=datetime.datetime.fromisoformat(presentday_str)
        yesterday = presentday - datetime.timedelta(1)
        Editdata_contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=yesterday.strftime('%d %m %Y')
        date=yesterday.strftime('%d %m %Y')
        build_editdata()
        page.update()

    def next_date_dp():
        presentday_str='-'.join(list((Editdata_contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value).split())[::-1])
        presentday=datetime.datetime.fromisoformat(presentday_str)
        tomorrow = presentday + datetime.timedelta(1)
        if tomorrow>datetime.datetime.today():
            pass
        else:
            Editdata_contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=tomorrow.strftime('%d %m %Y')
            date=tomorrow.strftime('%d %m %Y')
            build_editdata()
            page.update()




    def change_analysis_format():
        if analysis_dropdown.value=="Day":
            Analysis_Contents.controls[0]=Analysis_Daily_Contents.controls[0]
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=datetime.datetime.now().strftime("%d %m %Y")
            show_daily_analysis(datetime.datetime.now().strftime("%d %m %Y"))
        if analysis_dropdown.value=="Week":
            Analysis_Contents.controls[0]=Analysis_Weekly_Contents.controls[0]
        if analysis_dropdown.value=="Month":
            Analysis_Contents.controls[0]=Analysis_Monthly_Contents.controls[0]
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=datetime.datetime.now().strftime("%m")
            show_monthly_analysis(datetime.datetime.now().strftime("%m"))
        page.update()
    
    def change_date(e):
        # page.views[-1].controls[0].content.controls[1].controls[0].content.controls[1].content.value=Text(date_picker.value.strftime("%d %m %y"))
        Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=(date_picker.value.strftime("%d %m %Y"))
        Editdata_contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=(date_picker.value.strftime("%d %m %Y"))
        date=date_picker.value.strftime("%d %m %Y")
        show_daily_analysis(date)
        build_editdata()
        page.update()
    
    date_picker = DatePicker(
        on_change=change_date,
        on_dismiss=lambda _:print("dismissed"),
        first_date=datetime.datetime(2024,1,1),
        current_date=datetime.datetime.today(),
        last_date=datetime.datetime.today(),
    )

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
        if Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value-1:
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value-=1
        page.update()

    def next_week():
        nextweek=Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value+1
        if database.get_week_no(datetime.datetime.now().strftime("%d %m %Y"))>=nextweek and next_week<53:
            Analysis_Contents.controls[0].contenDatePict.controls[1].controls[0].content.controls[1].content.value=nextweek
        page.update()

    def previous_month():
        previousmonth=int(Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value)-1
        if previousmonth>0:
            previousmonth=str(previousmonth)
            if len(previousmonth)==1:
                previousmonth='0'+previousmonth
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=previousmonth
            show_monthly_analysis(previousmonth)
        page.update()

    def next_month():
        nextmonth=int(Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value)+1
        if int(datetime.datetime.now().strftime("%m"))>=nextmonth and nextmonth<=12:
            nextmonth=str(nextmonth)
            if len(nextmonth)==1:
                nextmonth='0'+nextmonth
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=nextmonth
            show_monthly_analysis(str(nextmonth))
        page.update()

    show_daily_analysis(date)
    rebuild_category_container()
    build_editdata()

    # show_daily_analysis(month)
    analysis_dropdown.value="Day"

    # print(month)

    
    page.on_route_change= change_route #when the route changes this function is called
    page.overlay.append(date_picker)


    page.add(container)
flet.app(target=main)
