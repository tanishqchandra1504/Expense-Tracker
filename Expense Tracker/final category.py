import flet
from flet import *

def main(page: Page):
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'
    PINK = '#eb06ff'

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

    page.padding = 0

    # First page
    first_page_contents = Container(
        content=Column(
            controls=[Row(alignment='spaceBetween',
                         controls=[IconButton(on_click=lambda e: shrink(e),
                                             content=Icon(icons.ARROW_FORWARD)),
                                  IconButton(on_click=lambda _: page.go('/Dataput'),
                                             content=Icon(icons.ADD))]
                         )
                     ]
        )
    )

    page_1 = Container(expand=True,
                       bgcolor=BG,
                       padding=20,
                       content=Column(
                           controls=[Container(height=17),
                                    IconButton(on_click=lambda e: restore(e),
                                               content=Icon(icons.ARROW_BACK)),
                                    Container(height=17),
                                    Row(controls=[TextButton('Analysis', icon=icons.ANALYTICS_SHARP, on_click=lambda _: page.go('/Analysis'))]),
                                    Container(height=17),
                                    Row(controls=[TextButton('Categories', icons.CATEGORY_SHARP, on_click=lambda _: page.go('/Categories'))]),
                                    Container(height=17),
                                    Row(controls=[TextButton('Dataput', icon=icons.DATA_ARRAY_SHARP, on_click=lambda _: page.go('/Dataput'))]),
                                    Container(height=17),
                                    Row(controls=[TextButton('Settings', icon=icons.SETTINGS, on_click=lambda _: page.go('/Settings'))]),
                                    Container(height=17),
                                    Row(controls=[TextButton('Exit', icon=icons.EXIT_TO_APP_SHARP, on_click=lambda _: page.go('/Exit'))])
                                    ]
                       )
                       )

    page_2 = Row(alignment='end',  # when animation happens it should move to right , default left
                 controls=[
                     Container(expand=True,
                               bgcolor=FG,
                               animate=animation.Animation(600, AnimationCurve.DECELERATE),
                               animate_scale=animation.Animation(400, AnimationCurve.DECELERATE),
                               padding=padding.only(top=50, left=20,
                                                   right=20, bottom=5),
                               content=Column(
                                   controls=[
                                       first_page_contents
                                   ]
                               )
                               )
                 ]
                 )

    container = Container(expand=True,
                          bgcolor=BG,
                          content=Stack(
                              controls=[
                                  page_1,
                                  page_2
                              ]
                          )
                          )

    category_list = []
    category_colors = []
    category_container = Column(
        controls=[])

    # Pop-up box
    dialog = None

    def add_category(e):
        new_category = category_input.value
        new_color = category_color_dropdown.value
        if new_category and new_color:
            if new_category in category_list:
                show_duplicate_dialog(new_category)
            else:
                category_list.append(new_category)
                category_colors.append(new_color)
                add_category_row(new_category, new_color)
                category_input.value = ""
                category_color_dropdown.value = None
                category_input.on_submit = add_category  # Reset the on_submit function
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
                    Text(category),
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
        )
    )
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

            category_list[category_index] = new_category
            category_colors[category_index] = color_options[new_color_index]

            # Rebuild the entire category container
            rebuild_category_container()

            category_input.value = ""
            category_color_dropdown.value = None
            category_input.on_submit = add_category  # Reset the on_submit function
            page.update()

        category_input.on_submit = update_category
        category_input.focus()  # Set focus to the text field
        page.update()

    def delete_category(category):
        category_index = category_list.index(category)

        def confirm_delete(choice):
            if choice == 'yes':
                category_list.pop(category_index)
                category_colors.pop(category_index)
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
        options=dropdown_options
    )

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

    Dataput_contents = Row(
        controls=[Container(expand=True,
                           bgcolor=FG,
                           padding=padding.only(top=50, left=20,
                                               right=20, bottom=5),
                           content=Column(controls=[
                               Row(
                                   controls=[IconButton(on_click=lambda _: page.go('/'),
                                                       content=Icon(icons.CLOSE_ROUNDED))])
                           ]
                           )
                           )
                  ]
              )

    Analysis_Contents = Row(
        controls=[Container(expand=True,
                           bgcolor=FG,
                           padding=padding.only(top=50, left=20,
                                               right=20, bottom=5),
                           content=Column(controls=[
                               Row(
                                   controls=[IconButton(on_click=lambda _: page.go('/'),
                                                       content=Icon(icons.CLOSE_ROUNDED))])
                           ]
                           )
                           )
                  ]
              )

    Settings_Contents = Row(
        controls=[Container(expand=True,
                           bgcolor=FG,
                           padding=padding.only(top=50, left=20,
                                               right=20, bottom=5),
                           content=Column(controls=[
                               Row(
                                   controls=[IconButton(on_click=lambda _: page.go('/'),
                                                       content=Icon(icons.CLOSE_ROUNDED))])
                           ]
                           )
                           )
                  ]
              )

    Exit_Contents = Row(
        controls=[Container(expand=True,
                           bgcolor=FG,
                           padding=padding.only(top=50, left=20,
                                               right=20, bottom=5),
                           content=Column(controls=[
                               Row(
                                   controls=[IconButton(on_click=lambda _: page.go('/'),
                                                       content=Icon(icons.CLOSE_ROUNDED))])
                           ]
                           )
                           )
                  ]
              )

    # routing info
    pages = {'/': View('/', [container]),
             '/Dataput': View('/Dataput', [Container(
                 expand=True,
                 bgcolor=FG,
                 content=Dataput_contents
             )]), '/Analysis': View('/Analysis', [Container(
                 expand=True,
                 bgcolor=FG,
                 content=Analysis_Contents
             )]), '/Categories': View('/Categories', [Container(
                 expand=True,
                 bgcolor=FG,
                 content=Category_contents
             )]),
             '/Settings': View('/Settings', [Container(
                 expand=True,
                 bgcolor=FG,
                 content=Settings_Contents
             )]),
             '/Exit': View('/Exit', [Container(
                 expand=True,
                 bgcolor=FG,
                 content=Exit_Contents
             )])}

    # Route functions
    def shrink(e):
        page_2.controls[0].expand = False
        page_2.controls[0].width = page.width / 2
        page_2.controls[0].scale = transform.Scale(0.8, alignment.center_right)
        page_2.controls[0].border_radius = 25
        page_2.update()

    def restore(e):
        page_2.controls[0].width = page.width
        page_2.controls[0].scale = transform.Scale(1, alignment.center_right)
        page_2.controls[0].border_radius = None
        page_2.update()

    def change_route(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
        )
        page.views[-1].padding = 0  # permanently sets page padding to zero even when pages are changed
        page.update()

    page.on_route_change = change_route  # when the route changes this function is called

    page.add(container)

flet.app(target=main)