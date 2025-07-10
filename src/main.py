import flet as ft
import random
import time

def main(page: ft.Page):
    page.title = "Игра Найди пары"
    page.window_height = 710
    page.window_width = 910
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    number_of_single_cards = 20
    image_page = "https://picsum.photos/id/"

    def make_cards(number_of_single_cards):
        card_deck_with_duplicates = \
            [f"{i}_A" for i in range(number_of_single_cards)] + \
            [f"{i}_B" for i in range(number_of_single_cards)]
        random.shuffle(card_deck_with_duplicates)
        return card_deck_with_duplicates

    idx_of_cards = make_cards(number_of_single_cards)
    list_of_pairs = []
    find = []

    def start_game(e):
        e.control.disabled = True
        global start_time
        start_time = time.time()

        for i in range(len(idx_of_cards)):
            row_board.controls[i].content = None
            row_board.controls[i].bgcolor = ft.Colors.AMBER
            row_board.controls[i].border_radius = ft.border_radius.all(10)
            row_board.controls[i].disabled = False
        page.update()

    def match_pairs(e):
        if len(list_of_pairs) == 2 or not start_button.disabled:
            return

        num = e.control.data
        idx = idx_of_cards[num].split('_')[0]
        index_a = idx_of_cards.index(f"{idx}_A")
        index_b = idx_of_cards.index(f"{idx}_B")
        index_of_image = idx_of_cards[num].split("_")[0]

        if len(list_of_pairs) < 2:
            e.control.content = ft.Image(src=f"{image_page+'1'+index_of_image}/100",
                                        border_radius=ft.border_radius.all(10))
            if idx_of_cards[num] not in list_of_pairs:
                list_of_pairs.append(idx_of_cards[num])
            page.update()

        if len(list_of_pairs) == 2:
            a = int(list_of_pairs[0].split('_')[0])
            b = int(list_of_pairs[1].split('_')[0])

            if a == b:
                time.sleep(0.4)
                for index in (index_a, index_b):
                    row_board.controls[index].disabled = True
                    row_board.controls[index].content = None
                    row_board.controls[index].bgcolor = ft.Colors.BLACK
                find.append(index_a)
                if len(find) == number_of_single_cards:
                    stop_time = time.time()
                    start_button.text = f"Время: \n{round(stop_time - start_time, 0)} \nсекунд"
                    page.update()
                page.update()
                list_of_pairs.clear()
            else:
                time.sleep(1)
                flip_a = idx_of_cards.index(list_of_pairs[0])
                flip_b = idx_of_cards.index(list_of_pairs[1])
                for index in (flip_a, flip_b):
                    row_board.controls[index].content = None
                    row_board.controls[index].bgcolor = ft.Colors.AMBER
                list_of_pairs.clear()
                page.update()

    def board(idx_of_cards):
        card_images = []
        for num in range(len(idx_of_cards)):
            index_of_image = idx_of_cards[num].split("_")[0]
            card_images.append(
                ft.Container(
                    content=None,
                    width=100,
                    height=100,
                    bgcolor=ft.Colors.AMBER,
                    border_radius=ft.border_radius.all(10),
                    data=num,
                    on_click=match_pairs
                )
            )
        return card_images

    row_board = ft.Row(wrap=True, controls=board(idx_of_cards))
    start_button = ft.ElevatedButton(text="Начать игру", width=100, height=100, on_click=start_game)

    page.add(
        ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(value="Найди пары", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                row_board,
                start_button
            ]
        )
    )

ft.app(main)