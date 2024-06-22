from shiny import App, reactive, render, ui
from shiny.ui import div, h1, head_content, tags
from pathlib import Path
import pandas as pd
import plotly.express as px
from shinywidgets import output_widget, render_widget
from activity_analysis import type1_data, type2_data, type3_data, type4_data, type5_data, type6_data
#from search_suggestions import give_search_result
from htmltools import HTML
import plotly.graph_objects as go
import plotly.subplots as sp
# from search_history_finder import getFilteredCounts, predict_upcoming_values, getImportantInfo
import numpy as np
import matplotlib.pyplot as plt

import meegle_main
import play_store
import google_maps
import youtube




# do przekopiowania do swojego pliku i na końcu wywalić
def colored_letters(word):
    return HTML("".join(f'<span class="letter-{i}">{letter}</span>' for i, letter in enumerate(word)))


main_page = meegle_main.main_page_fun()

play_store_page = play_store.play_store_div()

maps_page = google_maps.maps_div()

youtube_page = youtube.youtube_div()

activity_page = div(
    div(
        div(
            ui.img(src="left_arrow.png", id="small_button"),
            ui.img(src="right_arrow.png", id="small_button"),
            ui.img(src="reload.png", id="small_button"),
            id="fun_buttons"
        ),
        div(
            ui.input_text(label="", id="url3", value="https://meegle.analytics.com"),
            id="url_div"
        ),
        id="header_div"
    ),
    div(
        div(
            # ui.input_action_button("button_dots", HTML('<p class="button"> ...<br>...<br>...</p>')),
            div(
                ui.input_action_button(id="menu_button", label="", style="height: 40px; width: 40px;"),
                ui.img(src="menu.png", id="menu_image"),
                id="menu_button_div"
            ),
            id="menu_div"
        ),
        id="lower_header_div"
    ),
    div(
        div(
            ui.h3("Przeglądaj wykaz swojej aktywności, ze wszystkich aplikacji od Google"),
            ui.h6("Po prostu wybierz programy oraz interesujące Cię urządzenia a my zrobimy pracę za Ciebie.",
                  style="font-weight: bold"),
            id="activity_title"
        ),

        div(
            div(
                ui.input_action_button(id="chrome_activity_button", label="", style="height: 70px; width: 70px;"),
                ui.img(src="chrome.png", id="chrome_image_activity"),
                id="first_app_to_choose_activity"
            ),
            div(
                ui.input_action_button(id="playstore_activity_button", label="", style="height: 70px; width: 70px;"),
                ui.img(src="playstore.png", id="playstore_image_activity"),
                id="second_app_to_choose_activity"
            ),
            div(
                ui.input_action_button(id="youtube_activity_button", label="", style="height: 70px; width: 70px;"),
                ui.img(src="youtube.png", id="youtube_image_activity"),
                id="third_app_to_choose_activity"
            ),
            div(
                ui.input_action_button(id="gmail_activity_button", label="", style="height: 70px; width: 70px;"),
                ui.img(src="gmail.png", id="gmail_image_activity"),
                id="fourth_app_to_choose_activity"
            ),
            div(
                ui.input_action_button(id="photos_activity_button", label="", style="height: 70px; width: 70px;"),
                ui.img(src="photos.png", id="photos_image_activity"),
                id="fifth_app_to_choose_activity"
            ),

            id="apps_to_choose_activity"
        ),

        div(

            div(

                div(

                    div(

                        ui.h5("zakres analizy:"),

                        # domyslnie wspolna, pozniej do zmiany, w zaleznosci od klikniecia
                        div(
                            ui.input_action_button(id="btn_activity_type_changer", label="wspólna",
                                                   style="height: 50px; width: 150px;"),
                            id="btn_activity_type_changer_div"
                        ),
                        id="sub_panel_main_left_chooser_together_activity"
                    ),
                    div(
                        ui.h5("uwzględniane urządzenia:"),
                        ui.input_checkbox("smartphone_activity", "telefon komórkowy"),
                        ui.input_checkbox("pc_activity", "komputer osobisty"),
                        ui.input_checkbox("smartphone_pc_activity", "wspólne"),

                        # jezeli wystarczy nam czasu to zamienimy checboxy na buttony

                        id="sub_panel_main_left_chooser_devices_activity"
                    ),

                    id="sub_panel_main_left_chooser_activity"
                ),
                div(
                    # do usuniecia pozniej

                    ui.h5("Po zaznaczeniu wykresu tutaj będzi można ustawić dodatkowe parametry"),
                    id="sub_panel_main_left_additional_activity"
                ),

                id="sub_panel_main_left_activity"
            ),
            div(

                div(

                    ui.layout_sidebar(
                        ui.sidebar(
                            ui.input_action_button(id="plot_1_chooser", label="plot_1_chooser",
                                                   style="height: 10%; width: 55%; margin-left:auto; margin-right: auto"),

                            ui.h6("Wybierz zakres ustawień", style="margin-left: auto; margin-right: auto;"),

                            ui.input_slider("range_days_plot1", "Wybierz zakres interesujących Cię dni:",
                                            min=1, max=30,
                                            value=[1, 30]),

                            width="100%;"
                        ),
                        output_widget("activity_plot_1", width="120%;", height="120%;"), height="100%;"

                    ),
                    id="activity_plot_1_space"
                ),
                div(
                    ui.layout_sidebar(
                        ui.sidebar(
                            ui.input_action_button(id="plot_2_chooser", label="plot_2_chooser",
                                                   style="height: 10%; width: 55%; margin-left:auto; margin-right: auto"),

                            ui.h6("Wybierz zakres ustawień", style="margin-left: auto; margin-right: auto;"),

                            ui.input_checkbox("month_comparison_second_plot", "Porównywanie poprzedniego miesiąca",
                                              False),
                            ui.output_ui("value"),

                            width="100%;"
                        ),
                        output_widget("activity_plot_2", width="120%;", height="120%;"), height="100%;"

                    ),
                    id="activity_plot_2_space"
                ),
                div(

                    ui.layout_sidebar(
                        ui.sidebar(
                            ui.input_action_button(id="plot_3_chooser", label="plot_3_chooser",
                                                   style="height: 10%; width: 55%; margin-left:auto; margin-right: auto"),

                            ui.h6("Wybierz zakres ustawień", style="margin-left: auto; margin-right: auto;"),

                            ui.input_slider("range_days_plot3", "Wybierz zakres interesujących Cię dni:",
                                            min=1, max=7,
                                            value=[1, 7]),

                            width="100%;"
                        ),
                        output_widget("activity_plot_3", width="120%;", height="120%;"), height="100%;"

                    ),

                    id="activity_plot_3_space"
                ),
                div(

                    ui.layout_sidebar(
                        ui.sidebar(
                            ui.input_action_button(id="plot_4_chooser", label="plot_4_chooser",
                                                   style="height: 10%; width: 55%; margin-left:auto; margin-right: auto"),

                            ui.h6("Wybierz zakres ustawień", style="margin-left: auto; margin-right: auto;"),

                            ui.input_slider("range_days_plot4", "Wybierz zakres interesujących Cię dni:",
                                            min=1, max=30,
                                            value=[1, 30]),

                            width="100%;"
                        ),
                        ui.output_ui("activity_plot_4", width="120%;", height="120%;"), height="100%;"

                    ),

                    id="activity_plot_4_space"
                ),
                div(
                    ui.layout_sidebar(
                        ui.sidebar(
                            ui.input_action_button(id="plot_5_chooser", label="plot_5_chooser",
                                                   style="height: 10%; width: 55%; margin-left:auto; margin-right: auto"),

                            ui.h6("Wybierz zakres ustawień", style="margin-left: auto; margin-right: auto;"),

                            ui.input_slider("range_hours_plot5", "Wybierz zakres interesujących Cię godzin:",
                                            min=0, max=23,
                                            value=[0, 23]),
                            ui.input_slider("range_minutes_plot5", "Wybierz zakres interesujących Cię minut:",
                                            min=0, max=59,
                                            value=[0, 59]),

                            width="100%;"
                        ),
                        output_widget("activity_plot_5", width="120%;", height="120%;"),
                        ui.output_ui("activity_plot_5_potential", width="120%;", height="120%;"), height="100%;"

                    ),

                    id="activity_plot_5_space"
                ),
                div(

                    ui.layout_sidebar(
                        ui.sidebar(
                            ui.input_action_button(id="plot_6_chooser", label="plot_6_chooser",
                                                   style="height: 10%; width: 55%; margin-left:auto; margin-right: auto"),

                            ui.h6("Wybierz zakres ustawień", style="margin-left: auto; margin-right: auto;"),

                            ui.input_slider("range_days_plot6", "Wybierz zakres interesujących Cię dni:",
                                            min=1, max=30,
                                            value=[1, 30]),

                            width="100%;"
                        ),
                        ui.output_ui("activity_plot_6", width="120%;", height="120%;"), height="100%;"

                    ),

                    id="activity_plot_6_space"
                ),

                # tutaj dodajemy obszar na 6 wykresow do analizy
                id="sub_panel_main_right_activity"
            ),

            id="main_activity_container"
        ),

        id="master_div"
    ),
    div(
        id="footer_div"
    ),
    id="body_div"
)

chrome_page = div(
    div(
        div(
            ui.img(src="left_arrow.png", id="small_button"),
            ui.img(src="right_arrow.png", id="small_button"),
            ui.img(src="reload.png", id="small_button"),
            id="fun_buttons"
        ),
        div(
            ui.input_text(label="", id="url3", value="https://meegle.com/chrome"),
            id="url_div"
        ),
        id="header_div"
    ),
    div(
        div(
            # ui.input_action_button("button_dots", HTML('<p class="button"> ...<br>...<br>...</p>')),
            div(
                ui.input_action_button(id="menu_button", label="", style="height: 40px; width: 40px;"),
                ui.img(src="menu.png", id="menu_image"),
                id="menu_button_div"
            ),
            id="menu_div"
        ),
        id="lower_header_div"
    ),
    div(
        div(
            div(
                div(
                    ui.h1("Szukaj z", style="padding-top: 20px; margin-top: 20px;"),
                    id="logo_type_1"
                ),
                div(
                    ui.img(src="chrome.png", id="chrome_image_additional"),
                    id="logo_type_2"
                ),

                id="chrome_left_side_top"
            ),
            div(
                div(
                    ui.input_text(label="Wpisz nazwę strony", id="site_name", value=""),
                    id="site_name_div"
                ),
                div(
                    ui.input_action_button(id="search_chrome_button", label="Search",
                                           style="height: 45px; width: 130px;"),
                    id="search_name_div"
                ),
                ui.input_date_range("dateNext", "Wybierz zakres czasu:",
                                    start="2023-01-01", end="2023-12-16",
                                    min="2023-01-01", max="2023-12-16"),

                id="chrome_left_side_bottom"
            ),
            div(

                ui.output_ui("data_page", width="120%;", height="120%;"), height="100%;",
                id="chrome_info_holder"
            ),
            id="chrome_left_side"
        ),
        div(

            div(
                output_widget("site_analysis", width="100%;", height="120%;"),
                id="chrome_right_side_top"
            ),
            div(
                output_widget("site_prediction_analysis", width="100%;", height="120%;"),
                id="chrome-right_side_bottom"
            ),

            id="chrome_right_side"
        ),

        id="master_div"
    ),
    div(
        id="footer_div"
    ),
    id="body_div"
)

app_ui = ui.page_fluid(
    head_content(
        tags.style((Path(__file__).parent / "style.css").read_text()),
    ),
    {"id": "main-content"},
    ui.navset_card_tab(
        ui.nav("Meegle", main_page, value="meegle", icon=""),
        ui.nav("Play Store", play_store_page),
        ui.nav("Aktywność", activity_page),
        ui.nav("Chrome", chrome_page),
        ui.nav("Maps", maps_page),
        ui.nav('Youtube', youtube_page),
        id="tabset"
    ),
)


def server(input, output, session):
    #gabi youtube
    x=reactive.Value(0)


    @output
    @render_widget
    def youtube_plot():
        return youtube.youtube_charts(input)

    @output
    @render.text
    def comments():
        return youtube.comments_count_output()

    @output
    @render.text
    def title_of_video():
        return youtube.video_title(input)

    @output
    @render.text
    def which_person():
        return youtube.which_person()

    @output
    @render.text
    def how_many_subscribers():
        return youtube.how_many_subscribers(input)


    @render.ui
    @reactive.event(input.switch1)
    # @reactive.event(input.switch2)
    def update_switch2():
        ui.update_switch(input.switch2, value= not input.switch1())
        # ui.update_switch(input.switch2, label='hey',value=True)


    @render.ui
    @reactive.event(input.switch2)
    def update_switch1():
        ui.update_switch(input.switch1, value=not input.switch2())

    @output
    @render.text
    def description_text():
        return youtube.description_text(input)



    # @render.ui
    # @reactive.event(input.switch1)
    # def update_switch2():
    #     if input.switch1():
    #         ui.update_switch(input.switch2, value=False)
    #
    # @render.ui
    # @reactive.event(input.switch2)
    # def update_switch1():
    #     if input.switch2():
    #         ui.update_switch(input.switch1, value=False)





    # Ola - play store
    @output
    @render_widget
    def histogram():
        return play_store.histogram_play_store(input)

    @output
    @render_widget
    def wordcloud():
        return play_store.wordcloud_play_store(input)





    # Ola - google maps
    filtered_df = reactive.Value(None)

    @reactive.Effect
    @reactive.event(input.year_input, input.month_input)
    def _():
        df = google_maps.return_df()
        if input.year_input() == "WSZYSTKIE" and input.month_input() != "WSZYSTKIE":
            filtered_df.set(df[(df['Month'] == input.month_input())])
        elif input.year_input() != "WSZYSTKIE" and input.month_input() == "WSZYSTKIE":
            filtered_df.set(df[(df['Year'] == input.year_input())])
        elif input.year_input() != "WSZYSTKIE" and input.month_input() != "WSZYSTKIE":
            filtered_df.set(df[(df['Year'] == input.year_input()) & (df['Month'] == input.month_input())])
        else:
            filtered_df.set(df)

    @output
    @render_widget
    def map():
        return google_maps.return_map(filtered_df.get())

    # @output
    # @render.ui
    # @reactive.event(input.search_chrome_button)
    # def data_page():
    #     our_tag_list = ui.TagList()
    #
    #     beg_data = str(input.dateNext()[0])
    #     end_data = str(input.dateNext()[1])
    #
    #     looking_data = getImportantInfo([beg_data, end_data], input.site_name())
    #
    #     total_entries = str(round(looking_data[0], 2))
    #     avg_day = str(round(looking_data[1], 2))
    #     avg_month = str(round(looking_data[2], 2))
    #
    #     our_tag_list.append(ui.h5("Informacji na temat rejestrowanych wejść:", style="font-weight: bold;"))
    #     our_tag_list.append(ui.h6("Łączna liczba aktywności: " + total_entries))
    #     our_tag_list.append(ui.h6("Średnia dzienna liczba aktywności: " + avg_day))
    #     our_tag_list.append(ui.h6("Średnia miesięczna liczba aktywności: " + avg_month))
    #
    #     return our_tag_list

    # @output
    # @render_widget
    # def site_analysis():
    #
    #     if input.search_chrome_button() % 2 == 1:
    #         beg_data = str(input.dateNext()[0])
    #         end_data = str(input.dateNext()[1])
    #
    #         looking_data = getFilteredCounts([beg_data, end_data],
    #                                          input.site_name())
    #
    #         data_for_plot = pd.DataFrame(looking_data)
    #         data_for_plot['exact_date'] = pd.to_datetime(data_for_plot['exact_date'])
    #         data_for_plot = data_for_plot.sort_values(by="exact_date")
    #
    #         fig = px.line(data_for_plot, x='exact_date', y='Count', labels={'Count': 'Count'},
    #                       title='Line Plot of Count over Time')
    #
    #         return fig

    # @output
    # @render_widget
    # def site_prediction_analysis():
    #
    #     if input.search_chrome_button() % 2 == 1:
    #         beg_data = str(input.dateNext()[0])
    #         end_data = str(input.dateNext()[1])
    #
    #         looking_data = getFilteredCounts([beg_data, end_data],
    #                                          input.site_name())
    #         prediction_data = predict_upcoming_values(looking_data)
    #
    #         data_for_plot = pd.DataFrame(prediction_data)
    #
    #         data_for_plot['ds'] = pd.to_datetime(data_for_plot['ds'])
    #
    #         data_for_plot = data_for_plot[data_for_plot['ds'] >= '2024-01-01']
    #
    #         data_for_plot = data_for_plot.sort_values(by="ds")
    #
    #         fig = px.line(data_for_plot, x='ds', y='yhat_upper', labels={'yhat_upper': 'yhat_upper'},
    #                       title='Line Plot prediction over Time')
    #
    #         return fig

    # @output
    # @render.ui
    # @reactive.event(input.search)
    # def search_result():
    #
    #     user_text = input.search()
    #
    #     suggestion_list = give_search_result(user_text)
    #
    #     our_tag_list = ui.TagList()
    #
    #     our_tag_list.append(ui.h6(str(suggestion_list)))
    #
    #     return our_tag_list

    choose_1_plot = reactive.Value(False)
    choose_2_plot = reactive.Value(False)
    choose_3_plot = reactive.Value(False)
    choose_4_plot = reactive.Value(False)
    choose_5_plot = reactive.Value(False)
    choose_6_plot = reactive.Value(False)

    chooser_1_apps = reactive.Value([])
    chooser_2_apps = reactive.Value([])
    chooser_3_apps = reactive.Value([])
    chooser_4_apps = reactive.Value([])
    chooser_5_apps = reactive.Value([])
    chooser_6_apps = reactive.Value([])

    # put this value into method, to choose plot data
    logged_person = reactive.Value(0)

    @reactive.Effect
    @reactive.event(input.person_1_button)
    def change_logged_1():
        logged_person.set(1)
        ui.update_text("url", value="https://meegle.com/main_page/igorr")
        ui.update_text("url2", value="https://meegle.com/playstore/igorr")
        ui.update_text("url3", value="https://meegle.analytics.com/igorr")
        ui.update_text("url4", value="https://meegle.com/chrome/igorr")
        #ui.update_text("url5", value="https://meegle.com/youtube/igorr")

        ui.remove_ui("#popup_window")
        ui.remove_ui("#locker_button_div")

    @reactive.Effect
    @reactive.event(input.person_2_button)
    def change_logged_2():
        logged_person.set(2)
        ui.update_text("url", value="https://meegle.com/main_page/gabrielam")
        ui.update_text("url2", value="https://meegle.com/playstore/gabrielam")
        ui.update_text("url3", value="https://meegle.analytics.com/gabrielam")
        ui.update_text("url4", value="https://meegle.com/chrome/gabrielam")
        #ui.update_text("url5", value="https://meegle.com/youtube/gabrielam")

        ui.remove_ui("#popup_window")
        ui.remove_ui("#locker_button_div")

    @reactive.Effect
    @reactive.event(input.person_3_button)
    def change_logged_1():
        logged_person.set(3)
        ui.update_text("url", value="https://meegle.com/main_page/samsela")
        ui.update_text("url2", value="https://meegle.com/playstore/samsela")
        ui.update_text("url3", value="https://meegle.analytics.com/samsela")
        ui.update_text("url4", value="https://meegle.com/chrome/samsela")
        #ui.update_text("url5", value="https://meegle.com/youtube/samsela")

        ui.remove_ui("#popup_window")
        ui.remove_ui("#locker_button_div")

    @output
    @render.text
    def txt():
        return str(choose_1_plot())

    @output
    @render.text
    def txt2():
        return str(chooser_1_apps())

    @output
    @render.text
    def txt3():
        return str(choose_2_plot())

    @output
    @render.text
    def txt4():
        return str(chooser_2_apps())

    @reactive.Effect
    @reactive.event(input.plot_1_chooser)
    def marked_1():
        choose_1_plot.set(not choose_1_plot())

        apps_list = []

        if choose_1_plot() and input.chrome_activity_button() % 2 == 1:
            if "Search" not in chooser_1_apps():
                apps_list.append("Search")
                apps_list.append("Chrome Sync")

        if choose_1_plot() and input.playstore_activity_button() % 2 == 1:
            if "Play" not in chooser_1_apps():
                apps_list.append("Play")

        if choose_1_plot() and input.youtube_activity_button() % 2 == 1:
            if "YouTube" not in chooser_1_apps():
                apps_list.append("YouTube")

        if choose_1_plot() and input.gmail_activity_button() % 2 == 1:
            if "Gmail" not in chooser_1_apps():
                apps_list.append("Gmail")

        if choose_1_plot() and input.photos_activity_button() % 2 == 1:
            if "Photos" not in chooser_1_apps():
                apps_list.append("Photos")

        chooser_1_apps.set(apps_list)

    @reactive.Effect
    @reactive.event(input.plot_2_chooser)
    def marked_2():
        choose_2_plot.set(not choose_2_plot())

        apps_list = []

        if choose_2_plot() and input.chrome_activity_button() % 2 == 1:
            if "Search" not in chooser_2_apps():
                apps_list.append("Search")
                apps_list.append("Chrome Sync")

        if choose_2_plot() and input.playstore_activity_button() % 2 == 1:
            if "Play" not in chooser_2_apps():
                apps_list.append("Play")

        if choose_2_plot() and input.youtube_activity_button() % 2 == 1:
            if "YouTube" not in chooser_2_apps():
                apps_list.append("YouTube")

        if choose_2_plot() and input.gmail_activity_button() % 2 == 1:
            if "Gmail" not in chooser_2_apps():
                apps_list.append("Gmail")

        if choose_2_plot() and input.photos_activity_button() % 2 == 1:
            if "Photos" not in chooser_2_apps():
                apps_list.append("Photos")

        chooser_2_apps.set(apps_list)

    @reactive.Effect
    @reactive.event(input.plot_3_chooser)
    def marked_3():
        choose_3_plot.set(not choose_3_plot())

        apps_list = []

        if choose_3_plot() and input.chrome_activity_button() % 2 == 1:
            if "Search" not in chooser_3_apps():
                apps_list.append("Search")
                apps_list.append("Chrome Sync")

        if choose_3_plot() and input.playstore_activity_button() % 2 == 1:
            if "Play" not in chooser_3_apps():
                apps_list.append("Play")

        if choose_3_plot() and input.youtube_activity_button() % 2 == 1:
            if "YouTube" not in chooser_3_apps():
                apps_list.append("YouTube")

        if choose_3_plot() and input.gmail_activity_button() % 2 == 1:
            if "Gmail" not in chooser_3_apps():
                apps_list.append("Gmail")

        if choose_3_plot() and input.photos_activity_button() % 2 == 1:
            if "Photos" not in chooser_3_apps():
                apps_list.append("Photos")

        chooser_3_apps.set(apps_list)

    @reactive.Effect
    @reactive.event(input.plot_4_chooser)
    def marked_4():
        choose_4_plot.set(not choose_4_plot())

        apps_list = []

        if choose_4_plot() and input.chrome_activity_button() % 2 == 1:
            if "Search" not in chooser_4_apps():
                apps_list.append("Search")
                apps_list.append("Chrome Sync")

        if choose_4_plot() and input.playstore_activity_button() % 2 == 1:
            if "Play" not in chooser_4_apps():
                apps_list.append("Play")

        if choose_4_plot() and input.youtube_activity_button() % 2 == 1:
            if "YouTube" not in chooser_4_apps():
                apps_list.append("YouTube")

        if choose_4_plot() and input.gmail_activity_button() % 2 == 1:
            if "Gmail" not in chooser_4_apps():
                apps_list.append("Gmail")

        if choose_4_plot() and input.photos_activity_button() % 2 == 1:
            if "Photos" not in chooser_4_apps():
                apps_list.append("Photos")

        chooser_4_apps.set(apps_list)

    @reactive.Effect
    @reactive.event(input.plot_5_chooser)
    def marked_5():
        choose_5_plot.set(not choose_5_plot())

        apps_list = []

        if choose_5_plot() and input.chrome_activity_button() % 2 == 1:
            if "Search" not in chooser_5_apps():
                apps_list.append("Search")
                apps_list.append("Chrome Sync")

        if choose_5_plot() and input.playstore_activity_button() % 2 == 1:
            if "Play" not in chooser_5_apps():
                apps_list.append("Play")

        if choose_5_plot() and input.youtube_activity_button() % 2 == 1:
            if "YouTube" not in chooser_5_apps():
                apps_list.append("YouTube")

        if choose_5_plot() and input.gmail_activity_button() % 2 == 1:
            if "Gmail" not in chooser_5_apps():
                apps_list.append("Gmail")

        if choose_5_plot() and input.photos_activity_button() % 2 == 1:
            if "Photos" not in chooser_5_apps():
                apps_list.append("Photos")

        chooser_5_apps.set(apps_list)

    @reactive.Effect
    @reactive.event(input.plot_6_chooser)
    def marked_6():
        choose_6_plot.set(not choose_6_plot())

        apps_list = []

        if choose_6_plot() and input.chrome_activity_button() % 2 == 1:
            if "Search" not in chooser_6_apps():
                apps_list.append("Search")
                apps_list.append("Chrome Sync")

        if choose_6_plot() and input.playstore_activity_button() % 2 == 1:
            if "Play" not in chooser_6_apps():
                apps_list.append("Play")

        if choose_6_plot() and input.youtube_activity_button() % 2 == 1:
            if "YouTube" not in chooser_6_apps():
                apps_list.append("YouTube")

        if choose_6_plot() and input.gmail_activity_button() % 2 == 1:
            if "Gmail" not in chooser_6_apps():
                apps_list.append("Gmail")

        if choose_6_plot() and input.photos_activity_button() % 2 == 1:
            if "Photos" not in chooser_6_apps():
                apps_list.append("Photos")

        chooser_6_apps.set(apps_list)

    @reactive.Effect
    def _():
        if input.menu_button() % 2 == 1:

            div1 = div(

                ui.h6("Wybierz konto użytkownika:", style="font-weight: bold; font-size: 15px; "
                                                          "margin-left:auto, margin-right: auto; color: grey; padding-top: 10px;"),

                div(
                    div(
                        ui.img(src="ILetter.png", id="ILetter_login"),
                        id="first_person_login_left"
                    ),
                    div(
                        ui.h6("Igor Rudolf"),
                        id="first_person_login_right"
                    ),

                    ui.input_action_button(id="person_1_button", label="",
                                           style="height: 40px; width: 270px; padding-top: -78px; margin-top: -78px;"),

                    id="first_person_login_div"
                ),
                div(
                    div(
                        ui.img(src="GLetter.png", id="GLetter_login"),
                        id="second_person_login_left"
                    ),
                    div(
                        ui.h6("Gabriela Majstrak"),
                        id="second_person_login_right"
                    ),

                    ui.input_action_button(id="person_2_button", label="",
                                           style="height: 40px; width: 270px; padding-top: -78px; margin-top: -78px;"),

                    id="second_person_login_div"
                ),
                div(
                    div(
                        ui.img(src="ALetter.png", id="ALetter_login"),
                        id="third_person_login_left"
                    ),
                    div(
                        ui.h6("Aleksandra Samsel"),
                        id="third_person_login_right"
                    ),

                    ui.input_action_button(id="person_3_button", label="",
                                           style="height: 40px; width: 270px; padding-top: -78px; margin-top: -78px;"),

                    id="third_person_login_div"
                ),

            )

            ui.insert_ui(
                div(
                    div1,

                    id="popup_window"),
                selector="#popup_window_div",
                where="beforeEnd",
            )
        elif input.menu_button() > 0:
            pass
            ui.remove_ui("#popup_window")


    @output
    @render_widget
    def activity_plot_1():

        beg_day = int(input.range_days_plot1()[0])
        end_day = int(input.range_days_plot1()[1])

        if choose_1_plot():
            list_of_apps = chooser_1_apps.get()

            df_activity_1 = type1_data([beg_day, end_day], list_of_apps)
            fig = px.line(df_activity_1, x="Day", y="Count", color="Product Name", markers=True,
                          title='Product Count Over Days', width=700, height=300)
            return fig
        else:
            df_activity_1 = type1_data([beg_day, end_day], [])
            fig = px.line(df_activity_1, x="Day", y="Count", color="Product Name", markers=True,
                          title='Product Count Over Days')
            return fig

    @output
    @render.ui
    def value():
        return input.month_comparison_second_plot()

    @output
    @render_widget
    def activity_plot_2():

        beg_day = int(input.range_days_plot1()[0])
        end_day = int(input.range_days_plot1()[1])

        if choose_2_plot():
            list_of_apps = chooser_2_apps.get()

            if input.month_comparison_second_plot():
                needed_data = type2_data(True, list_of_apps)

                df1 = needed_data[0]
                df2 = needed_data[1]

                hist_data_df1 = [df1[df1['Product Name'] == product]['Count'] for product in
                                 df1['Product Name'].unique()]

                group_labels_df1 = df1['Product Name'].unique()

                # Create a subplot for df1
                fig = sp.make_subplots(rows=2, cols=1, subplot_titles=['Hourly Distribution of Counts - DataFrame 1',
                                                                       'Hourly Distribution of Counts - DataFrame 2'],
                                       shared_xaxes=True, vertical_spacing=0.1)

                # Add histograms for each product in df1
                for data, label in zip(hist_data_df1, group_labels_df1):
                    fig.add_trace(go.Histogram(x=data, name=label, nbinsx=15), row=1, col=1)

                hist_data_df2 = [df2[df2['Product Name'] == product]['Count'] for product in
                                 df2['Product Name'].unique()]
                group_labels_df2 = df2['Product Name'].unique()

                # Add histograms for each product in df2
                for data, label in zip(hist_data_df2, group_labels_df2):
                    fig.add_trace(go.Histogram(x=data, name=label, nbinsx=15), row=2, col=1)

                fig.update_layout(barmode='overlay', showlegend=False, width=700, height=300,
                                  xaxis=dict(title='Count'), yaxis=dict(title='Frequency'))

                return fig

            else:

                needed_data = type2_data(False, list_of_apps)

                df = needed_data

                hist_data = [df[df['Product Name'] == product]['Count'] for product in df['Product Name'].unique()]

                group_labels = df['Product Name'].unique()

                # Create a figure with subplots
                fig = go.Figure()

                # Add histograms for each product
                for data, label in zip(hist_data, group_labels):
                    fig.add_trace(go.Histogram(x=data, name=label, nbinsx=15))

                # Update layout
                fig.update_layout(barmode='overlay', title='Hourly Distribution of Counts',
                                  xaxis_title='Count', yaxis_title='Frequency')

                return fig
        else:
            df_activity_2 = type1_data([beg_day, end_day], [])
            fig = px.line(df_activity_2, x="Day", y="Count", color="Product Name", markers=True,
                          title='Product Count Over Days')
            return fig

    @output
    @render_widget
    def activity_plot_3():

        beg_day = int(input.range_days_plot3()[0])
        end_day = int(input.range_days_plot3()[1])

        if choose_3_plot():

            list_of_apps = chooser_3_apps.get()

            needed_data = type3_data([beg_day, end_day], list_of_apps)

            fig = px.bar(needed_data, x="Day Name", y="Count", color="Product Name", title="Day Name Counts")

            return fig

        else:
            df_activity_3 = type1_data([beg_day, end_day], [])
            fig = px.line(df_activity_3, x="Day", y="Count", color="Product Name", markers=True,
                          title='Product Count Over Days')
            return fig

    @output
    @render.ui
    @reactive.event(input.plot_4_chooser)
    def activity_plot_4():
        beg_day = int(input.range_days_plot4()[0])
        end_day = int(input.range_days_plot4()[1])

        if choose_4_plot():
            list_of_apps = chooser_4_apps.get()

            needed_data = type4_data([beg_day, end_day], list_of_apps)

            out_tag_list = ui.TagList()

            list_of_apps_pd = needed_data

            rows_amount = len(list_of_apps_pd.axes[0])

            for i in range(rows_amount):
                element_name = str(list_of_apps_pd['Product Name'].iloc[i])
                needed_time = str(list_of_apps_pd['Time Difference'].iloc[i])

                out_tag_list.append(ui.h6(element_name + ' ' + needed_time,
                                          style="font-weight: bold; margin-left:auto; margin-right: auto;"))

            return out_tag_list

        else:
            df_activity_4 = type1_data([beg_day, end_day], [])
            fig = px.line(df_activity_4, x="Day", y="Count", color="Product Name", markers=True,
                          title='Product Count Over Days')
            return fig

    @output
    @render_widget
    def activity_plot_5():
        beg_day = int(input.range_days_plot4()[0])
        end_day = int(input.range_days_plot4()[1])

        if choose_5_plot():
            list_of_apps = chooser_5_apps.get()

            if len(list_of_apps) > 1 or len(list_of_apps) == 0:
                pass
            else:
                product = list_of_apps[0]

                hours_beg = int(input.range_hours_plot5()[0])
                hours_end = int(input.range_hours_plot5()[1])

                minutes_beg = int(input.range_minutes_plot5()[0])
                minutes_end = int(input.range_minutes_plot5()[1])

                needed_data = type5_data([hours_beg, hours_end], [minutes_beg, minutes_end], product)

                fig = go.Figure(go.Heatmap(
                    z=needed_data['Count'],
                    x=needed_data['hour'],
                    y=needed_data['minute'],
                    colorscale='Viridis',
                ))

                fig.update_layout(
                    xaxis=dict(title='Hour'),
                    yaxis=dict(title='Minute'),
                    title='Heatmap of Counts by Hour and Minute for ' + str(product)
                )

                return fig


        else:
            df_activity_5 = type1_data([beg_day, end_day], [])
            fig = px.line(df_activity_5, x="Day", y="Count", color="Product Name", markers=True,
                          title='Product Count Over Days')
            return fig

    @output
    @render.ui
    @reactive.event(input.plot_5_chooser)
    def activity_plot_5_potential():
        list_of_apps = chooser_5_apps.get()

        if len(list_of_apps) == 0 or len(list_of_apps) > 1:
            return ui.TagList(
                ui.h6("Należy wybrać tylko jedną aplikację")
            )

    @output
    @render.ui
    @reactive.event(input.plot_6_chooser)
    def activity_plot_6():
        beg_day = int(input.range_days_plot1()[0])
        end_day = int(input.range_days_plot1()[1])

        if choose_6_plot():
            list_of_apps = chooser_6_apps.get()

            needed_data = type6_data([beg_day, end_day], list_of_apps)

            our_tag_list = ui.TagList()

            rows_amount = len(needed_data.axes[0])

            for i in range(rows_amount):
                previous_product = str(needed_data['previous_product'].iloc[i])
                next_product = str(needed_data['next_product'].iloc[i])
                amount = str(needed_data['change_count'].iloc[i])

                our_tag_list.append(ui.h6(previous_product + '-' + next_product + ' amount: ' + amount,
                                          style='font-weight: bold; margin-left: auto; margin-right: auto;'))

            return our_tag_list

        else:
            df_activity_6 = type1_data([beg_day, end_day], [])
            fig = px.line(df_activity_6, x="Day", y="Count", color="Product Name", markers=True,
                          title='Product Count Over Days')
            return fig


www_dir = Path(__file__).parent / "www"

app = App(app_ui, server, static_assets=www_dir)
