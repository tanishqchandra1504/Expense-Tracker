import flet as ft
import database
import datetime
import copy

def daily_piechart(date):
    cat_dict=database.show_categorywise_daily_expense(date)
    if len(cat_dict)==0:
        return ft.PieChart(
            sections=[
                ft.PieChartSection(
                    value=100,
                    title="No data to display",
                    title_position=0,
                    color="grey",
                    radius=100,
                )
            ],
            center_space_radius=0,
        )
    # date in str format
    normal_radius = 100
    hover_radius = 110
    normal_title_style = ft.TextStyle(
        size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD,shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
    )
    hover_title_style = ft.TextStyle(
        size=14,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
    )
    def chart_event(e:ft.PieChartEvent):
        for id,section in enumerate(piechart.sections):
            if id==e.section_index:
                section.radius=hover_radius
                section.title_style=hover_title_style
            else: 
                section.radius=normal_radius
                section.title_style=normal_title_style
            piechart.update()

    piechart=ft.PieChart(
        sections=[],
        sections_space=0,
        center_space_radius=0,
        on_chart_event=chart_event,
        expand=True,
    )
    totalamt=sum([x[0] for x in cat_dict.values()])
    for cat,amtclr in cat_dict.items():
        piechart.sections.append(
            ft.PieChartSection(
                    value=amtclr[0],
                    title=cat+f"-{amtclr[0]/totalamt*100}"[:5]+"%",
                    title_position=1,
                    title_style=normal_title_style,
                    color=amtclr[1],
                    radius=normal_radius,
                ),
        )
    return piechart

def home_piechart(date):
    cat_dict=database.show_categorywise_daily_expense(date)
    if len(cat_dict)==0:
        return [ft.PieChart(
            sections=[
                ft.PieChartSection(
                    value=100,
                    title="No data to display",
                    title_position=0,
                    color="grey",
                    radius=100,
                )
            ],
            center_space_radius=0,
        )]
    # date in str format
    normal_radius = 100
    hover_radius = 110
    normal_title_style = ft.TextStyle(
        size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD,shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
    )
    hover_title_style = ft.TextStyle(
        size=16,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
    )
    def chart_event(e:ft.PieChartEvent):
        for id,section in enumerate(piechart.sections):
            if id==e.section_index:
                section.radius=hover_radius
                section.title_style=hover_title_style
            else: 
                section.radius=normal_radius
                section.title_style=normal_title_style
            piechart.update()

    piechart=ft.PieChart(
        sections=[],
        sections_space=0,
        center_space_radius=0,
        on_chart_event=chart_event,
        expand=True,
    )
    
    totalamt=sum([x[0] for x in cat_dict.values()])

    cat_list=list(cat_dict.keys())

    for cat,amtclr in cat_dict.items():
        piechart.sections.append(
            ft.PieChartSection(
                    value=amtclr[0],
                    title=cat+f"-{amtclr[0]/totalamt*100}"[:4]+"%",
                    title_position=1.3,
                    title_style=normal_title_style,
                    color=amtclr[1],
                    radius=normal_radius,
                    data=cat,
                ),
        )
    legends=ft.Container(
        content=ft.Column(
            controls=[
                #catcolor and catname
            ]
        )
    )
    cat_dict=dict(sorted(cat_dict.items(),key=lambda x:x[1][0],reverse=True))
    for cat in cat_dict:
        legends.content.controls.append(
            ft.Row(controls=[
                ft.Container(
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,controls=[ft.Text(value=cat,color="black"),ft.Text(value=cat_dict[cat][0],color="black")]),
                bgcolor=cat_dict[cat][1],
                padding=ft.padding.only(top=3,bottom=3,left=20,right=10),
                border_radius=5,
                expand=True,
                shadow=ft.BoxShadow(spread_radius=1,blur_radius=1,color=ft.colors.BLACK54)
                )
            ]))

    chartofday=ft.Text("Pie of the Day:",color="white",size=20,weight=ft.FontWeight.BOLD)

    totalsofday=ft.Column(expand=False,height=100,controls=[
                                        ft.Container(bgcolor=ft.colors.TRANSPARENT,expand=True,content=ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(value="Total expense today : ",color=ft.colors.WHITE,size=18,italic=True),
                                                ft.Text(value=str(database.sumofday(date) if database.sumofday(date)!=False else 0)+" ",color=ft.colors.WHITE,size=20,italic=True),
                                            ]
                                        )),
                                        ft.Container(bgcolor=ft.colors.TRANSPARENT,expand=True,content=ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(value="Total expense this week : ",color=ft.colors.WHITE,size=18,italic=True),
                                                ft.Text(value=str(database.sumofweek(database.get_week_no(date)))+" ",color=ft.colors.WHITE,size=20,italic=True),
                                            ]
                                        )),
                                        ft.Container(bgcolor=ft.colors.TRANSPARENT,expand=True,content=ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(value="Total expense this month : ",color=ft.colors.WHITE,size=18,italic=True),
                                                ft.Text(value=str(database.sumofmonth(date[3:]))+" ",color=ft.colors.WHITE,size=20,italic=True),
                                            ]
                                        )),])

    return [chartofday,piechart,legends,ft.Divider(height=50,thickness=2,color="grey600"),totalsofday,ft.Container(height=25)]

class State:
    toggle = True

s = State()

def monthly_linechart(mmyyyy):
    month=mmyyyy[:2]
    m=int(mmyyyy[:2])
    year=mmyyyy[3:]
    y=int(mmyyyy[2:])
    days=0
    if m in [1,3,5,7,8,10,12]: days=31
    elif m in [4,6,9,11]: days=30
    else:
        if y%400==0 or (y%4==0!=y%100):
            days=29
        else: days=28

    date=datetime.datetime.fromisoformat(year+'-'+month+'-01')

    data_1=[ft.LineChartData(data_points=[],
                           color=ft.colors.with_opacity(1, ft.colors.GREEN),
            below_line_bgcolor=ft.colors.with_opacity(0.2, ft.colors.LIGHT_GREEN),
            stroke_width=4,
            curved=False,
            stroke_cap_round=True,)]
    

    lst=[]
    for i in range(1,days+1):
        total=database.sumofday(date.strftime("%d %m %Y"))
        if total!=False:
            data_1[0].data_points.append(ft.LineChartDataPoint(i,total))
            lst.append(total)
        date+= datetime.timedelta(days=1)
    #intercept to check if any data is present in the entire month
    if len(lst)==0:
        return ft.Container(
            expand=True,
            bgcolor="grey",
            gradient=ft.LinearGradient(colors=["green","bluegrey700"]),
            border_radius=30,
            content=ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[
                ft.Row(alignment="center",controls=[ft.Text("No data to display",size=30,weight=ft.FontWeight.BOLD)])])
        )
    Max=max(lst)
    Max=int(Max)
    
    data_2=copy.deepcopy(data_1)
    data_2[0].curved=True

    chart=ft.LineChart(
        data_series=data_1,
        border=ft.Border(
            bottom=ft.BorderSide(4, ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE)),
        ),
        left_axis=ft.ChartAxis(
            labels=[
            ],
            labels_size=40,
            # title=ft.Text("Amount Spent",weight=ft.FontWeight.BOLD,italic=True,color=ft.colors.WHITE)
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
            ],
            labels_size=32,
            title=ft.Text("DAYS OF MONTH",weight=ft.FontWeight.BOLD,italic=True)
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
        min_y=0,
        max_y=Max,
        min_x=0,
        max_x=days+1,
        # animate=5000,
        expand=True,
    )
    
    for i in range(1,days+1):
        chart.bottom_axis.labels.append(ft.ChartAxisLabel(
                        value=i,
                        label=ft.Text(
                                i,
                                size=16,
                                weight=ft.FontWeight.NORMAL,
                                color=ft.colors.with_opacity(0.6, ft.colors.LIGHT_GREEN),
                            ),
                    ),)
        
    for i in range(0,Max+1):
        chart.left_axis.labels.append(ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(f'{i}', size=14, weight=ft.FontWeight.BOLD,color=ft.colors.LIGHT_GREEN),
                ))
        
    def toggle_data(e):
        if s.toggle:
            chart.data_series = data_2
            # chart.data_series[0].point = True
        else:
            chart.data_series = data_1
        s.toggle = not s.toggle
        chart.update()

    return ft.Container(expand=True,content=ft.Column(controls=[
        ft.IconButton(ft.icons.REFRESH, on_click=toggle_data), chart
    ]))


def weekly_linechart(weekno):
    #return start date of week
    date=datetime.datetime(2023,12,31)
    for i in range(weekno):
        date=date+datetime.timedelta(7)
    data_1=[ft.LineChartData(data_points=[],
                           color=ft.colors.with_opacity(1, ft.colors.GREEN),
            below_line_bgcolor=ft.colors.with_opacity(0.2, ft.colors.LIGHT_GREEN),
            stroke_width=4,
            curved=False,
            stroke_cap_round=True,)]
    
    lst=[]
    for i in range(1,8):
        total=database.sumofday(date.strftime("%d %m %Y"))
        if total!=False:
            data_1[0].data_points.append(ft.LineChartDataPoint(i,total))
            lst.append(total)
        date+= datetime.timedelta(days=1)

    #intercept to check if any data is present in the entire month, returns container with message if no data is present in entire month
    if len(lst)==0:
        return ft.Container(
            expand=True,
            bgcolor="grey",
            gradient=ft.LinearGradient(colors=["green","bluegrey700"]),
            border_radius=30,
            content=ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=[
                ft.Row(alignment="center",controls=[ft.Text("No data to display",size=30,weight=ft.FontWeight.BOLD)])])
        )
    
    Max=int(max(lst))
    
    data_2=copy.deepcopy(data_1)
    data_2[0].curved=True

    chart=ft.LineChart(
        data_series=data_1,
        border=ft.Border(
            bottom=ft.BorderSide(4, ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE)),
        ),
        left_axis=ft.ChartAxis(
            labels=[
            ],
            labels_size=40,
            # title=ft.Text("Amount Spent",weight=ft.FontWeight.BOLD,italic=True,color=ft.colors.WHITE)
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
            ],
            labels_size=32,
            title=ft.Text("WEEKDAYS",weight=ft.FontWeight.BOLD,italic=True)
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
        min_y=0,
        max_y=Max,
        min_x=0,
        max_x=8,
        # animate=5000,
        expand=True,
    )
    daysofweek=['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    for i in range(1,8):
        chart.bottom_axis.labels.append(
            ft.ChartAxisLabel(
                value=i,
                label=ft.Text(value=daysofweek[i-1],color=ft.colors.LIGHT_GREEN,size=16)
            )
        )
    for i in range(0,Max+1):
        chart.left_axis.labels.append(ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(f'{i}', size=14, weight=ft.FontWeight.BOLD,color=ft.colors.LIGHT_GREEN),
                ))
    def toggle_data(e):
        if s.toggle:
            chart.data_series = data_2
            # chart.data_series[0].point = True
        else:
            chart.data_series = data_1
        s.toggle = not s.toggle
        chart.update()

    return ft.Container(expand=True,content=ft.Column(controls=[
        ft.IconButton(ft.icons.REFRESH, on_click=toggle_data),chart
    ]))