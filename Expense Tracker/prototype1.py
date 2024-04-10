import flet
from flet import *
import datetime


def main(page:Page):
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'
    PINK = '#eb06ff'



    page.padding=0
    
    #First page
    first_page_contents=Container(
        content=Column(
            controls=[Row(alignment='spaceBetween',
                        controls=[IconButton(on_click=lambda e:shrink(e),
                                            content=Icon(icons.ARROW_FORWARD)),
                                  IconButton(on_click=lambda _:page.go('/Dataput'),
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
                            Row(controls=[TextButton('Dataput',icon=icons.DATA_ARRAY_SHARP,on_click=lambda _:page.go('/Dataput'))]),
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
                        first_page_contents
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
    
    Category_contents=Row(
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
    
    Dataput_contents=Row(
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
    #.controls[0].content.controls[1].controls[0].content.controls[1].content.value=Text(date_picker.value.strftime("%d %m %y"))
    Analysis_Contents=Row(
        controls=[Container(expand=True,
                            bgcolor=FG,
                            padding=padding.only(top=50,left=20,right=20,bottom=5),
                            content=Column(controls=[
                                            Row(
                                                controls=[
                                                    IconButton(
                                                        on_click=lambda _:page.go('/'),
                                                        content=Icon(icons.CLOSE_ROUNDED)
                                                    )

                                                ]
                                            ),

                                            #daily
                                            Row(
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
                                                                        # content=date_picker.value,
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

                                            Container(
                                                        width=200,
                                                        height=200,

                                                        #graph
                                                    ),

                                            Column(
                                                controls=[
                                                    Row(
                                                        controls=[
                                                            Card(
                                                                expand=True,
                                                                height=100,
                                                                # border=border.all(0.85, "white54"),
                                                                # border_radius=8,
                                                                color=BG,
                                                                content=(
                                                                    Row(
                                                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                        controls=[
                                                                            #cate color, cate name, amount
                                                                            
                                                                        ]
                                                                    )
                                                                ),
                                                            ),
                                                            
                                                        ]
                                                        
                                                    ),
                                                    Row(
                                                        controls=[
                                                            Card(
                                                                expand=True,
                                                                height=100,
                                                                # border=border.all(0.85, "white54"),
                                                                # border_radius=8,
                                                                color="bluegrey",
                                                                content=(
                                                                    Row(
                                                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                                        controls=[
                                                                            #cate color, cate name, amount
                                                                            
                                                                        ]
                                                                    )
                                                                ),
                                                            ),
                                                            
                                                        ]
                                                        
                                                    )
                                                ]
                                                
                                            )
                                        ]
                                    )
                        )
            ]
        )
    
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
    

    #routing info
    pages={'/':View('/',[container]),
            '/Dataput':View('/Dataput',[Container(
                expand=True,
                bgcolor=FG,
                content=Dataput_contents
                                  
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
        page_2.update()


    def restore(e):
        page_2.controls[0].width=page.width
        page_2.controls[0].scale=transform.Scale(1,alignment.center_right)
        page_2.update()

    def change_route(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
        )
        page.views[-1].padding=0 #permanently sets page padding to zero even when pages are changed
        page.update()



    def change_date(e):
        # page.views[-1].controls[0].content.controls[1].controls[0].content.controls[1].content.value=Text(date_picker.value.strftime("%d %m %y"))
        Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=(date_picker.value.strftime("%d %m %Y"))
        page.update()
    
    date_picker = DatePicker(
        on_change=change_date,
        on_dismiss=lambda _:print("hello"),
        first_date=datetime.datetime(2024,1,1),
        current_date=datetime.datetime.today(),
        last_date=datetime.datetime.today(),
    )

    def previous_date():

        presentday_str='-'.join(list((Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value).split())[::-1])
        presentday=datetime.datetime.fromisoformat(presentday_str)
        yesterday = presentday - datetime.timedelta(1)
        Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=yesterday.strftime('%d %m %Y')
        page.update()
    
    def next_date():

        presentday_str='-'.join(list((Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value).split())[::-1])
        presentday=datetime.datetime.fromisoformat(presentday_str)
        tomorrow = presentday + datetime.timedelta(1)
        Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=tomorrow.strftime('%d %m %Y')
        page.update()




    
    page.on_route_change= change_route #when the route changes this function is called
    page.overlay.append(date_picker)



    page.add(container)









flet.app(target=main)
