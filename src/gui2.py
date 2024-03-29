from flet import *
from main import main
from time import sleep

class progress_ring(object):
    def __init__(self, page: Page, *args, **kwargs):
        self.page = page
        self.progress_ring = ProgressRing()
        self.progress_ring.visible = False
        self.page.add(Column(
            [self.progress_ring],
            horizontal_alignment="center",
            alignment="center",
            width="100%",
            height="100%",
        ),)
        self.page.update()

    def __call__(self):
        self.progress_ring.visible = True
        self.page.update()

    def __del__(self):
        self.progress_ring.visible = False
        self.page.update()


def mainGUI(page: Page):
    page.title = "TOPINV - Gerador de Relatórios"
    page.window_resizable = False
    page.window_width = 300
    page.window_height = 380
    page.vertical_alignment = "center"
    page.update()

    def pick_template_result(e: FilePickerResultEvent):
        try:
            template_path = template_picker.result.files[0].path
            verify(template_path, "Template", "o")
            return template_path
        except Exception:
            open_Snack_Bar(page, "Houve um erro ao selecionar o template. Tente novamente.", bgcolor="orange")

    def pick_sheet_result(e: FilePickerResultEvent):
        try:
            sheet_path = sheet_picker.result.files[0].path
            verify(sheet_path, "Planilha", "a")
            return sheet_path
        except Exception:
            open_Snack_Bar(page, "Houve um erro ao selecionar a planilha. Tente novamente.", bgcolor="orange")

    def pick_destination_folder_result(e: FilePickerResultEvent):
        try:
            destination_folder_picker.value = e.path
            verify(destination_folder_picker.value, "Pasta de destino", "a")
            return destination_folder_picker.value
        except Exception:
            open_Snack_Bar(page, "Houve um erro ao selecionar a pasta de destino. Tente novamente.", bgcolor="orange")
        
    def open_Snack_Bar(page: Page, message: str, bgcolor: str):
        page.snack_bar = SnackBar(Text(message), bgcolor=bgcolor)
        page.snack_bar.open = True
        page.update()

    def start_process():
        try:
            open_Snack_Bar(page, "Criando relatórios...", bgcolor="blue")
            progress = progress_ring(page)
            progress()
            main_result = main(sheet_picker.result.files[0].path, destination_folder_picker.value, template_picker.result.files[0].path)

            if main_result:
                open_Snack_Bar(page, "Relatórios criados com sucesso!", bgcolor="green")
            else:
                open_Snack_Bar(page, "Erro: Relatórios não foram criados corretamente.", bgcolor="red")
        except Exception as e:
            print(f"Erro: {e}")
            

    def verify(selected_file, type: str, char: str):
        if selected_file != None:
            txt.value = f"{type} selecionad{char}!"
        else:
            txt.value = f"{type} não selecionad{char}!"

    txt = Text("")

    template_picker = FilePicker(on_result=pick_template_result)
    sheet_picker = FilePicker(on_result=pick_sheet_result)
    destination_folder_picker = FilePicker(on_result=pick_destination_folder_result)

    page.overlay.extend([template_picker, sheet_picker, destination_folder_picker])

    page.update()

    template_picker_button = ElevatedButton("Selecionar Template",
                                                on_click=lambda _: template_picker.pick_files(
                                                    allow_multiple=False,
                                                    file_type=FilePickerFileType.CUSTOM,
                                                    allowed_extensions=["docx"]
                                                    ),
                                              icon=icons.UPLOAD_FILE,
                                              disabled=page.web)
    
    sheet_picker_button = ElevatedButton("Selecionar planilha",
                                           on_click=lambda _: sheet_picker.pick_files(
                                               allow_multiple=False,
                                               file_type=FilePickerFileType.CUSTOM,
                                               allowed_extensions=["xlsx", "csv"]
                                               ),
                                           icon=icons.UPLOAD_FILE)
    
    destination_folder_picker_button = ElevatedButton("Selecionar pasta de destino",
                                                         on_click=lambda _: destination_folder_picker.get_directory_path(),
                                                         icon=icons.FOLDER_OPEN,
                                                         disabled=page.web)
    
    start_process_button = ElevatedButton("Iniciar Processo",
                                             on_click=lambda _: start_process(),
                                             icon=icons.PLAY_ARROW,)

    page.add(
        Row([template_picker_button]),
        Row([sheet_picker_button]),
        Row([destination_folder_picker_button, destination_folder_picker]),
        Row([start_process_button])
    )

    page.update()

    return page

app(target=mainGUI)