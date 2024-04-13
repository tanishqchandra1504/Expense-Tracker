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

    page.padding=0
    date=datetime.datetime.now().strftime("%d %m %Y")
    month=date[3:5]


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
        date=date_picker.value.strftime("%d %m %Y")
        show_daily_analysis(date)
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
            Analysis_Contents.controls[0].content.controls[1].controls[0].content.controls[1].content.value=nextweek
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
    # show_daily_analysis(month)
    analysis_dropdown.value="Day"
    # print(month)

    
    page.on_route_change= change_route #when the route changes this function is called
    page.overlay.append(date_picker)


    page.add(container)









flet.app(target=main)
