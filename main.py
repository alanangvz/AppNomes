import flet as ft
from models import db_execute, db_filtro_alchemy


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor=ft.colors.WHITE
        self.page.window.width=350
        self.page.window.height=450
        self.page.window.always_on_top
        self.page.window.left = 1180
        self.main_page()


    def add_pessoa(self, e, nome, idade):
        db_execute(f'INSERT INTO pessoas VALUES(?,?,?)', params=[None, nome, idade])
        self.input_nome.value = ''
        self.input_idade.value = ''
        self.btn_add.disabled = True
        self.btn_add.update()
        self.input_idade.update()
        self.input_nome.update()
        self.atualizar(e)
        
    def atualizar(self, e):
        nomes = self.nomes()
        self.page.controls.pop()
        self.page.add(nomes)
        self.page.update()
        
    def habilita_add(self, e):
        self.btn_add.disabled = False if self.input_nome.value and self.input_idade.value  else True
        self.btn_add.update()

    def del_pessoa(self, e, id):
        db_execute(f'DELETE FROM pessoas WHERE id={id}')
        self.atualizar(e)


    def topo(self):
        
        self.input_nome = ft.TextField(
            expand=True,
            hint_text='Digite o nome',
            on_change=self.habilita_add
        )

        self.input_idade = ft.TextField(
            expand=True,
            hint_text='Digite a idade',
            on_change=self.habilita_add
        )

        topo = ft.Row(
            controls=[
                self.input_nome,
                self.input_idade                
            ]
        )
        return topo

    def botoes(self):

        self.btn_add = ft.FilledButton(
                    expand=True,
                    text='Adicionar',                   
                    on_click=lambda e: self.add_pessoa(e, self.input_nome.value, self.input_idade.value),
                    disabled=True
                )

        botoes = ft.Row(
            controls=[
                btn_atu := ft.FilledButton(
                    expand=True,
                    text='Atualizar',
                    on_click=self.atualizar
                ),
                self.btn_add
            ]
        )
        return botoes

    def nomes(self):

        lista_pessoa = db_filtro_alchemy()

        def view_pessoa(nome, idade):
            view_pessoa = ft.Text(
                width=100,
                value=f'{nome}_{idade}'
            )
            return view_pessoa
        
        def btn_apagar(id, nome, idade):
            btn_apagar = ft.IconButton(
                icon=ft.icons.DELETE_FOREVER,
                icon_size=20,
                on_click=lambda e: self.del_pessoa(e, id)
            )
            return btn_apagar

        nomes = ft.Column(
            # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            height=self.page.height * 1,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Row(                                                                        
                    controls=[
                        view_pessoa(pessoa.nome, pessoa.idade),
                        btn_apagar(pessoa.id, pessoa.nome, pessoa.idade)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ) for pessoa in lista_pessoa
            ],
            spacing=0,  
        )
        return nomes



    def main_page(self):
        
        topo = self.topo()
        botoes = self.botoes()
        nomes = self.nomes()



        self.page.add(topo, botoes, nomes)
        


if __name__ == '__main__':
    ft.app(target=App) 