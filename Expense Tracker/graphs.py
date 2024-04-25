import flet as ft
import database

def daily_piechart(date):
    expense_list=database.show_daily_expense(date)
    if len(expense_list)==0:
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

    cat_dict={}
    for cat,clr,amt,d,w in expense_list:
        if cat in cat_dict:
            cat_dict[cat][0]+=amt
        else:
            cat_dict[cat]=[amt,clr]
    totalamt=sum([x[0] for x in cat_dict.values()])
    for cat,amtclr in cat_dict.items():
        piechart.sections.append(
            ft.PieChartSection(
                    value=amtclr[0],
                    title=cat+f" - {amtclr[0]}",
                    title_position=0.7,
                    title_style=normal_title_style,
                    color=amtclr[1],
                    radius=normal_radius,
                ),
        )
    return piechart

def home_piechart(date):
    expense_list=database.show_daily_expense(date)
    if len(expense_list)==0:
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

    cat_dict={}
    for cat,clr,amt,d,w in expense_list:
        if cat in cat_dict:
            cat_dict[cat][0]+=amt
        else:
            cat_dict[cat]=[amt,clr]
    totalamt=sum([x[0] for x in cat_dict.values()])

    cat_list=list(cat_dict.keys())

    for cat,amtclr in cat_dict.items():
        piechart.sections.append(
            ft.PieChartSection(
                    value=amtclr[0],
                    title=f"{amtclr[0]/totalamt*100}"[:4]+"%",
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

    for cat in cat_dict:
        legends.content.controls.append(
            ft.Row(controls=[

            ])
        )
    for cat in cat_dict:
        print(cat)
        legends.content.controls.append(
            ft.Row(controls=[
                ft.Container(
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,controls=[ft.Text(value=cat),ft.Text(value=cat_dict[cat][0])]),
                bgcolor=cat_dict[cat][1],
                padding=ft.padding.only(top=3,bottom=3,left=20,right=10),
                border_radius=5,
                expand=True,
                shadow=ft.BoxShadow(spread_radius=1,blur_radius=1,color=ft.colors.BLACK54)
                )
            ]))

    # legendchart=ft.Container(
    #     expand=True,
    #     content=ft.Column(
    #         controls=[
    #             piechart,
    #             legends
    #         ]
    #     )
    # )
    return [piechart,legends]