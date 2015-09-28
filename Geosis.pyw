
from tkinter import * 
from tkinter import filedialog, messagebox
from obspy import read
import matplotlib
matplotlib.use('TkAgg')                                                                  
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import os                                                                              
import numpy as np
from scipy import stats
import sys
import ast
                            

class Launcher(Tk):
    
    def __init__(self):

        Tk.__init__(self)
        self.geometry('640x400')
        self.title('Geosis v1.0')
        parentLauncher = Frame(self)
        parentLauncher.grid(row=0,column=0,sticky='nsew')
        barraDEmenu = Menu(self)
        self.configure(menu=barraDEmenu)
        menu_modulos=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Módulos',menu=menu_modulos)
        menu_modulos.add_command(label='Sispick',
                                      command= self.chamarSispick)
        menu_modulos.add_command(label='Siscon',
                                      command= self.chamarSiscon)
        menu_ajuda = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Ajuda',menu=menu_ajuda)
        menu_ajuda.add_command(label='Sobre o software',command = self.Sobre)

        try:
            
            photo = PhotoImage(file="%s/imagens/unb_geof.gif"%os.getcwd())
            self.iconbitmap("%s/imagens/terra1.ico"%os.getcwd())

        except:

            messagebox.showerror('',"Arquivos faltando na pasta 'imagens'")
            
        label = Label(parentLauncher,image=photo)
        label.image = photo
        label.grid(row=0,column=0,sticky='nsew')
        botaoSispick = Button(parentLauncher, text='sispick',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarSispick).grid(row=0,column=0,sticky='w')   
        botaosiscon = Button(parentLauncher, text='siscon',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarSiscon).grid(row=0,column=0,sticky='e')
        botaosisref = Button(parentLauncher, text='sisref',width=10,height=1,font=("Verdana", 12),
                              bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',command = self.chamarsisref).grid(row=0,column=0,padx=50)
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.fechar)

    def fechar(self):

        if messagebox.askyesno("Geosis", "Fechar o launcher?"):
            
            self.destroy()

        else:

            pass

    def chamarsisref(self):

        self.destroy()
        sisref()

    def chamarSispick(self):

        self.destroy()
        Sispick()

    def chamarSiscon(self):

        self.destroy()
        Siscon()

    def Sobre(self):

        root = Tk()
        root.geometry('630x300')
        root.title('Info')
        titulo = Label(root, text='Sobre o software',fg='green',font=("Helvetica", 14))
        root.resizable(0,0)
        root.mainloop()
        

class Sispick(Tk):
    
    def __init__(self):                         

        Tk.__init__(self)                       
        self.configure(background='#F3F3F3')
        self.geometry('800x600')
        self.wm_state('zoomed')
        self.title('Geosis - Sispick')               
        self.iconbitmap("%s/imagens/terra1.ico"%os.getcwd())
        
        self.frames = []                        
        self.figs = []                          
        self.axes = []                      
        self.telas = []                    
        self.listSource = []                    
        self.sts = []                        
        self.ticksLabel = []                    
        self.toolbars = []
        self.dadosNorms = []
        self.dadosCrus = []
        self.ganho = []
        self.filtros = []
        self.filtrosHP = []
        self.filtrosLP = []
        self.copiasCruas = []
        self.copiasNorms = []
        self.okpicks = []
        self.clips = []
        self.sombreamentos = []
        self.picks = []
        self.picksArts = []
        self.linhasArts = []
        self.conexoesPick = []
        self.ndados = []
        self.tracosMax = []
        self.temp = []
                          
        self.plotArts = {}
        self.sombArts = {}
        self.trClipados = {}
                         
        self.plotExiste = False                 
        self.pickMode = False                                                
        self.pickHappened = False               
        self.yinvertido = False
        self.seg2 = False
        self.normalizado = False
        self.optAberto = False
        self.pickAmostraAtivado = False

        self.eventCon = None                                          
        self.pagina = None
        self.recordlen = None                   
        self.valordx = None
        self.decisaoPontos = None
        self.ladoFill = 'positivo'
        self.fatorY = 0.8
        self.valorGanho = 2
        self.fatorLP = 0.8
        self.fatorHP = 3
        self.freqLP = []
        self.freqHP = []
        
        self.valorFigx = self.winfo_screenwidth()/80.50

        if self.winfo_screenheight() == 1080:
            
            self.valorFigy = self.winfo_screenheight()/93.10

        elif self.winfo_screenheight() == 768:

            self.valorFigy = self.winfo_screenheight()/99.74

        elif self.winfo_screenheight() == 1024:

            self.valorFigy = self.winfo_screenheight()/94.1

        elif self.winfo_screenheight() == 900:

            self.valorFigy = self.winfo_screenheight()/96.5

        elif self.winfo_screenheight() == 720:

            self.valorFigy = self.winfo_screenheight()/101.5

        else: # 800

            self.valorFigy = self.winfo_screenheight()/99
        
        self.parent = Frame(self,bg='#F3F3F3')
        self.parent.grid(row=0,column=0,sticky='nsew')
        barraDEmenu = Menu(self)
        self.configure(menu=barraDEmenu)
        menu_arquivo=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Arquivo',menu=menu_arquivo)
        menu_arquivo.add_command(label='Abrir                    Ctrl+A',
                                      command=self.abrir_pt1)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label='Salvar pick Seisimager (.vs)           Ctrl+S',
                                      command=self.salvarpick)
        menu_arquivo.add_command(label='Salvar pick Geosis (.gp)           Ctrl+S',
                                      command=self.salvargp)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label='Sair                         Alt+S',
                                      command=self.destroy)
        menu_visualizar = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Visualizaçao',menu=menu_visualizar)
        menu_visualizar.add_command(label='Proximo                Direita',
                                         command=self.nextpage)
        menu_visualizar.add_command(label='Anterior                Esquerda',
                                         command=self.backpage)
        menu_visualizar.add_separator()
        menu_visualizar.add_command(label='Inverter eixo y       I',
                                         command=self.backpage)
        menu_visualizar.add_separator()
        menu_visualizar.add_command(label='Diminuir eixo y      Baixo',
                                         command=self.menosy)
        menu_visualizar.add_command(label='Aumentar eixo y    Cima',
                                         command=self.maisy)
        menu_tracos = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Traços',menu=menu_tracos)
        menu_tracos.add_command(label='Dar ganho                                 Shift + Direita',
                                     command=self.ampup)
        menu_tracos.add_command(label='Retirar ganho                            Shift + Esquerda',
                                     command=self.ampdown)
        menu_tracos.add_separator()
        menu_tracos.add_command(label='Aplicar/Retirar normalizaçao       N',
                                     command=self.normalizar)
        menu_tracos.add_separator()
        menu_tracos.add_command(label='Aplicar/Retirar sombreamento    S',
                                     command=self.fill)
        menu_tracos.add_separator()
        menu_tracos.add_command(label='Clipar         C',
                                     command=self.clip)
        menu_editar = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Editar',menu=menu_editar)
        menu_editar.add_command(label='Ativar/Desativar pick                  P',
                                     command=self.ativarPick)
        menu_editar.add_command(label='Limpar plot                                L',
                                     command=self.limparplot)
        menu_editar.add_separator()
        menu_editar.add_command(label='Redefinir amostras      A',
                                 command=self.pickAmostra)
        menu_editar.add_command(label='Restaurar amostras originais      Alt + A',
                                         command=self.amostrasDefault)
        menu_editar.add_separator()
        menu_editar.add_command(label='Fechar seçao atual                     Ctrl+X',
                                     command=self.fecharPlot)
        menu_filtros = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Filtros',menu=menu_filtros)
        menu_filtros.add_command(label='Passa baixa          Ctrl+O',command=self.filtroLP)
        menu_filtros.add_command(label='Passa alta          Ctrl+O',command=self.filtroHP)
        menu_filtros.add_separator()
        menu_filtros.add_command(label='Remover filtros          Ctrl+O',command=self.removerFiltros)
        menu_opcoes = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Opçoes',menu=menu_opcoes)
        menu_opcoes.add_command(label='Opções de plot          Ctrl+O',command=self.configPlot)
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label='Editar cabeçalho          Ctrl+O',command = self.cabecalho)
        menu_ajuda = Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Ajuda',menu=menu_ajuda)
        menu_ajuda.add_command(label='Atalhos de teclado',command = lambda: print(''))
        Back = Button(self.parent, text='<',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = 'chartreuse3',activeforeground='white',
                      activebackground = 'chartreuse2', command = self.backpage).grid(row=0,column=0,sticky=W)
        Next = Button(self.parent, text='>',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = 'chartreuse3',activeforeground='white',
                      activebackground = 'chartreuse2', command = self.nextpage).grid(row=0,column=1,sticky=W)
        ampDown = Button(self.parent, text='-',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                              bg = 'gold2',activeforeground='white',
                         activebackground = 'yellow2', command = self.ampdown).grid(row=0,column=2,sticky=W)
        ampUp = Button(self.parent, text='+',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                            bg = 'gold2',activeforeground='white',
                       activebackground = 'yellow2', command = self.ampup).grid(row=0,column=3,sticky=W)
        menosY = Button(self.parent, text='- Y',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                             bg = 'DarkOrange2',activeforeground='white',
                            activebackground = 'orange2', command = self.menosy).grid(row=0,column=4,sticky=W)
        maisY = Button(self.parent, text='+Y',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                            bg = 'DarkOrange2',activeforeground='white',
                            activebackground = 'orange2', command = self.maisy).grid(row=0,column=5,sticky=W)
        Pick = Button(self.parent, text='P', bg = 'red3',font=("Arial", 10,'bold'),width = 4,
                           activebackground = 'red2',
                      activeforeground = 'white', command = self.ativarPick).grid(row=0,column=6,sticky=W)
        limpar = Button(self.parent, text='L', bg = 'snow2',font=("Arial", 10,'bold'),width = 4,
                           activebackground = 'snow',
                      activeforeground = 'black', command = self.limparplot).grid(row=0,column=7,sticky=W)
        inverttime = Button(self.parent, text='I',width = 4,font=("Arial", 10,'bold'),
                                 fg= 'black', bg = 'goldenrod4',activeforeground='white',
                            activebackground = 'gold3', command = self.invert).grid(row=0,column=8,sticky=W)
        normal = Button(self.parent, text='N',fg= 'black',font=("Arial", 10,'bold'),
                             width = 4, bg = 'purple2',activeforeground='white',
                            activebackground = 'DarkOrchid1', command = self.normalizar).grid(row=0,column=9,sticky=W)
        FILL = Button(self.parent, text='S',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = '#3065CE',activeforeground='white',
                            activebackground = '#5983D7', command = self.fill).grid(row=0,column=10,sticky=W)
        clipar = Button(self.parent, text='C',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = 'bisque4',activeforeground='white',
                            activebackground = 'bisque3', command = self.clip).grid(row=0,column=11,sticky=W)
        PA = Button(self.parent, text='PA',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = '#8CA9E4',activeforeground='white',
                            activebackground = '#C5D4F1', command = self.filtroHP).grid(row=0,column=12,sticky=W)
        PB = Button(self.parent, text='PB',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = '#FFACAA',activeforeground='white',
                            activebackground = '#FFD5D4', command = self.filtroLP).grid(row=0,column=13,sticky=W)
        RF = Button(self.parent, text='RF',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = '#6E7E40',activeforeground='white',
                            activebackground = '#8B9766', command = self.removerFiltros).grid(row=0,column=14,sticky=W)

        pickAmostras = Button(self.parent, text='A',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                           bg = '#999999',activeforeground='white',
                            activebackground = '#CCCCCC', command = self.pickAmostra).grid(row=0,column=15,sticky=W)
        FecharPlot = Button(self.parent, text='x', bg = 'gray3',font=("Arial", 10,'bold'),
                                 width = 4,fg='white', activebackground = 'gray30',
                            activeforeground = 'gold2', command = self.fecharPlot).grid(row=0,column=16,sticky=W)
        self.status = Label(self.parent,text = ' ', fg='red',font=("Helvetica", 12))
        self.status.grid(row=0,column=17,sticky=E)
        self.statusPA = Label(self.parent,text = ' ', fg='green',font=("Helvetica", 12))
        self.statusPA.grid(row=0,column=18,sticky=E)
        self.statusPB = Label(self.parent,text = ' ', fg='green',font=("Helvetica", 12))
        self.statusPB.grid(row=0,column=19,sticky=E)
        
        plt.rcParams['keymap.zoom'] = 'z,Z'
        plt.rcParams['keymap.back'] = 'v,V'
        plt.rcParams['keymap.home'] = 'ctrl+z,ctrl+Z'
        plt.rcParams['keymap.save'] = 'ctrl+i,ctrl+I'
        plt.rcParams['keymap.pan'] = 'm,M'
        self.bind('<Alt-s>', lambda x: self.destroy())
        self.bind('<Alt-S>', lambda x: self.destroy())
        self.bind('<Control-a>', lambda x: self.abrir_pt1())
        self.bind('<Control-A>', lambda x: self.abrir_pt1())
        self.bind('<Control-s>', lambda x: self.salvarpick())
        self.bind('<Control-S>', lambda x: self.salvarpick())
        self.bind('<Control-x>', lambda x: self.fecharPlot())
        self.bind('<Control-X>', lambda x: self.fecharPlot())
        self.bind('<Control-o>', lambda x: self.configPlot())
        self.bind('<Control-O>', lambda x: self.configPlot())
        self.bind('<Shift-Left>', lambda x: self.ampdown())
        self.bind('<Shift-Right>', lambda x: self.ampup())
        self.bind('<Up>', lambda x: self.maisy())
        self.bind('<Down>', lambda x: self.menosy())
        self.bind('i', lambda x: self.invert())
        self.bind('n', lambda x: self.normalizar())
        self.bind('s', lambda x: self.fill())
        self.bind('c', lambda x: self.clip())
        self.bind('I', lambda x: self.invert())
        self.bind('N', lambda x: self.normalizar())
        self.bind('S', lambda x: self.fill())
        self.bind('s', lambda x: self.fill())
        self.bind('C', lambda x: self.clip())
        self.bind('P', lambda x: self.ativarPick())
        self.bind('p', lambda x: self.ativarPick())
        self.bind('<Left>', lambda x: self.backpage())
        self.bind('<Right>', lambda x: self.nextpage())
        self.protocol("WM_DELETE_WINDOW", self.fechar)
    
        self.mainloop()

    def fechar(self):

        if messagebox.askyesno("Geosis - Sispick", "Sair do programa?"):

            self.destroy()

        else:

            pass

    def abrir_pt1(self):
        
        if self.plotExiste == False:
                    
            self.arquivos = sorted(filedialog.askopenfilenames(title='Abrir',filetypes=[('seg2','*.dat'),('segy','*.sgy'),
                                                                           ('mseed','*.mseed'),('Todos os arquivos','*.*')]))

            if len(self.arquivos) > 0:

                self.status.configure(text=' Abrindo %d arquivo(os). Aguarde...'%len(self.arquivos))

                try:
                
                    for i in range(len(self.arquivos)):

                        self.frame = Frame(self,bg='#F3F3F3')
                        self.frame.grid(row=1, column=0,sticky='nsew')
                        self.frames.append(self.frame)
                        fig = plt.figure(i,figsize=(self.valorFigx,self.valorFigy),facecolor='#F3F3F3')
                        self.figs.append(fig)
                        ax = self.figs[i].add_subplot(111)
                        self.axes.append(ax)
                        self.sts.append(read(self.arquivos[i]))
                        self.dadosCrus.append({})
                        self.dadosNorms.append({})
                        self.plotArts[i] = []
                        self.sombArts[i] = []
                        self.trClipados[i] = []
                        self.picks.append({})
                        self.picksArts.append({})
                        self.linhasArts.append({})
                        self.tracosMax.append({})
                        self.ndados.append(len(self.sts[i][0]))

                        try:
                            
                            self.listSource.append(self.sts[i][0].stats.seg2['SOURCE_LOCATION'])
                            self.seg2 = True

                        except:

                            messagebox.showinfo('','Posição de fonte de tiro não encontrada no cabeçalho. Para adicionar vá em Cabeçalho > Editar valores')
                            self.listSource.append(999)
                            self.seg2 = False
                            pass

                        try:
                            
                            self.valordx = float(self.sts[0][1].stats.seg2['RECEIVER_LOCATION'])-float(self.sts[0][0].stats.seg2['RECEIVER_LOCATION'])
                            self.seg2 = True

                        except:

                            self.seg2 = False
                            self.configDx()

                    self.abrir_pt2()

                except:

                    messagebox.showerror('','Erro na leitura do arquivo. Informações em Ajuda > Erros')
                    self.status.configure(text='')

            else:

                pass

        else:
        
            messagebox.showinfo('','Feche a seçao sismica atual para abrir uma nova')

    def abrir_pt2(self):

        for i in range(len(self.arquivos)):

            self.canais = len(self.sts[0])                      
            self.recordlen = self.sts[0][0].stats.endtime-self.sts[0][0].stats.starttime
            self.intervaloAmostragem = self.sts[0][0].stats.delta     
            self.ganho.append(1)
            self.clips.append(False)
            self.sombreamentos.append(False)
            self.filtros.append(False)
            self.copiasCruas.append(None)
            self.copiasNorms.append(None)
            self.freqLP.append(1000)
            self.freqHP.append(5)
            self.filtrosLP.append(False)
            self.filtrosHP.append(False)

            for j in range(self.canais):

                self.tracosMax[i][max(self.sts[i][j].data*(-1))] = j
            
            for j in range(self.canais):

                self.dadosCrus[i][j] = self.sts[i][j].data/max(self.tracosMax[i])
                self.dadosNorms[i][j] = self.sts[i][j].data/self.sts[i][j].data.max()
                self.trClipados[i].append([])
                self.okpicks.append(float(self.sts[i][0].stats.seg2['RECEIVER_LOCATION'])+self.valordx*j)
                self.ticksLabel.append(str(int(j*self.valordx)))
                traco, = self.axes[i].plot(self.dadosCrus[i][j][0:self.ndados[i]]*(-1)+float(self.sts[i][0].stats.seg2['RECEIVER_LOCATION'])+self.valordx*j,
                                           [self.sts[i][0].stats.delta*k for k in range(int(self.ndados[i]))],color='black')
                self.plotArts[i].append(traco)

            plt.figure(i)    
            plt.title(' %s | %d canais'%(os.path.basename(self.arquivos[i]),int(self.canais)))     
            plt.xlabel('Distância (m)')
            plt.ylabel('Tempo (s)')
            plt.ylim(0,self.sts[i][0].stats.delta*self.ndados[i])
            plt.xlim(float(self.sts[i][0].stats.seg2['RECEIVER_LOCATION'])-self.valordx,float(self.sts[i][-1].stats.seg2['RECEIVER_LOCATION'])+self.valordx)
            #plt.xticks(int(self.ticksLabel),self.ticksLabel)     
            tela = FigureCanvasTkAgg(self.figs[i], self.frames[i])
            self.telas.append(tela)
            self.telas[i].show()
            self.telas[i].get_tk_widget().pack(fill='both', expand=True)
            toolbar = NavigationToolbar2TkAgg(self.telas[i], self.frames[i])
            self.toolbars.append(toolbar)
            self.toolbars[i].update()
            self.telas[i]._tkcanvas.pack(fill='both', expand=True)

        self.status.configure(text=' ')
        self.frames[0].tkraise()
        self.pagina = 0
        plt.figure(self.pagina)

        def do(event):
                
            key_press_handler(event, self.telas[self.pagina], self.toolbars[self.pagina])
            
        self.figs[-1].canvas.mpl_connect('key_press_event', do)
        
        self.plotExiste = True
        self.yinvertido = False
        self.sombreamento = False
        self.normalizado = False

    def nextpage(self):
        
        if self.plotExiste == True and self.pagina < len(self.arquivos)-1:
            
            frame = self.frames[self.pagina+1]
            frame.tkraise()
            self.pagina += 1
            self.telas[self.pagina].show()

            if self.filtrosHP[self.pagina] == True:
                
                self.statusPA.configure(text = 'Passa alta: %.2f Hz'%float(self.freqHP[self.pagina]/self.fatorHP))

            if self.filtrosLP[self.pagina] == True:

                self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%float(self.freqLP[self.pagina]/self.fatorLP))

            if self.filtrosHP[self.pagina] != True:

                self.statusPA.configure(text = '')

            if self.filtrosLP[self.pagina] != True:
                
                self.statusPB.configure(text = '')
            
        else:
            
            pass

    def backpage(self):

        if self.plotExiste == True and self.pagina == 0:
                
             pass

        elif self.plotExiste == True and self.pagina != 0:
                
            frame = self.frames[self.pagina-1] 
            frame.tkraise()
            self.pagina -= 1
            self.telas[self.pagina].show()

            if self.filtrosHP[self.pagina] == True:
                
                self.statusPA.configure(text = 'Passa alta: %.2f Hz'%float(self.freqHP[self.pagina]/self.fatorHP))

            if self.filtrosLP[self.pagina] == True:

                self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%float(self.freqLP[self.pagina]/self.fatorLP))

            if self.filtrosHP[self.pagina] != True:

                self.statusPA.configure(text = '')

            if self.filtrosLP[self.pagina] != True:
                
                self.statusPB.configure(text = '')
            
        else:
            
            pass
                    
    def ativarPick(self):
        
        if self.plotExiste == True:

            if self.pickMode == False:

                self.pickMode = True
                self.status.configure(text=' Pick ativado',fg='blue')
                
                def pick(event):

                    try:

                        nearestMagnetValue = min(self.okpicks, key=lambda x: abs(event.xdata - x))
                        
                        if nearestMagnetValue in self.picks[self.pagina]:

                            self.picks[self.pagina][nearestMagnetValue] = event.ydata
                            self.picksArts[self.pagina][nearestMagnetValue].remove()
                            pickline = self.axes[self.pagina].hlines(event.ydata,nearestMagnetValue-1,
                                                                nearestMagnetValue+1,colors='r',linestyle='solid')
                            self.picksArts[self.pagina][nearestMagnetValue] = pickline
                            self.telas[self.pagina].show()

                            for i in range(len(self.arquivos)):

                                if i == self.pagina:

                                    pass

                                else:

                                    self.linhasArts[i][nearestMagnetValue].remove()
                                    linhasverdes = self.axes[i].hlines(event.ydata,nearestMagnetValue-1,
                                                                nearestMagnetValue+1,colors='green',linestyle='solid')
                                    self.linhasArts[i][nearestMagnetValue] = linhasverdes
                                    
                        else:
                            
                            pickline = self.axes[self.pagina].hlines(event.ydata,nearestMagnetValue-1,
                                                                nearestMagnetValue+1,colors='r',linestyle='solid')
                            self.picksArts[self.pagina].update({nearestMagnetValue:pickline})
                            self.picks[self.pagina].update({nearestMagnetValue:event.ydata})
                            self.telas[self.pagina].show()

                            for i in range(len(self.arquivos)):

                                if i == self.pagina:

                                    pass

                                else:

                                    linhasverdes = self.axes[i].hlines(event.ydata,nearestMagnetValue-1,
                                                                nearestMagnetValue+1,colors='green',linestyle='solid')
                                    self.linhasArts[i].update({nearestMagnetValue:linhasverdes})
                            
                            self.pickHappened = True

                    except:

                        pass
                
                for i in range(len(self.arquivos)):
                    
                    cid = self.figs[i].canvas.mpl_connect('button_press_event', pick)
                    self.conexoesPick.append(cid)

            else:

                for i in range(len(self.arquivos)):
                    
                    self.figs[i].canvas.mpl_disconnect(self.conexoesPick[i])
                    
                del self.conexoesPick[:]

                self.pickMode = False
                self.status.configure(text=' ',fg='red')
        
        else:

            pass

    def limparplot(self):

        if self.plotExiste == True:

            if len(self.picks[self.pagina]) > 0:

                if messagebox.askyesno("Geosis - Sispick", "Limpar picks do sismograma atual?"):

                    for i in self.picksArts[self.pagina].values():
                    
                        i.remove()

                    self.picks[self.pagina].clear()
                    self.picksArts[self.pagina].clear()
                    self.telas[self.pagina].show()

                    for i in range(len(self.arquivos)):

                        if i == self.pagina:

                            pass

                        else:

                            for j in self.linhasArts[i].values():

                                j.remove()

                        self.linhasArts[i].clear()
                        self.telas[i].show()

                else:

                    pass

            else:

                pass   

        else:

            pass
                    
    def fecharPlot(self):
          
        if self.plotExiste == True:

            if messagebox.askyesno("Geosis - Sispick", "Fechar o projeto atual?"):

                for i in self.frames:

                    i.destroy()

                for i in self.axes:

                    i.cla()

                for i in self.figs:

                    i.clf()

                del self.frames[:]
                del self.figs[:]
                del self.axes[:]
                del self.telas[:]
                del self.listSource[:]
                del self.sts[:]
                del self.ticksLabel[:]
                del self.toolbars[:]
                del self.stsNorms[:]
                del self.ganho[:]
                del self.filtros[:]
                del self.filtrosHP[:]
                del self.filtrosLP[:]
                del self.copiasCruas[:]
                del self.copiasNorms[:]
                del self.okpicks[:]
                del self.clips[:]
                del self.sombreamentos[:]
                del self.picks[:]
                del self.picksArts[:]
                del self.linhasArts[:]
                del self.conexoesPick[:]
                del self.freqLP[:]
                del self.freqHP[:]
                self.plotArts.clear()
                self.sombArts.clear()
                self.trClipados.clear()
                self.plotExiste = False                 
                self.pickMode = False                                                
                self.pickHappened = False               
                self.yinvertido = False
                self.seg2 = False
                self.normalizado = False
                self.optAberto = False
                self.eventCon = None                                          
                self.pagina = None
                self.recordlen = None                   
                self.valordx = None
                self.decisaoPontos = None
                self.ladoFill = 'positivo'
                self.fatorY = 0.3
                self.valorGanho = 1.5
                self.fatorLP = 0.8
                self.fatorHP = 1.5
                self.status.configure(text = '',fg='red')
                self.statusPA.configure(text = '', fg = 'green')
                self.statusPB.configure(text = '', fg = 'green')

            else:

                pass

        else:

            pass

    def conferidorIndividual(self):

        if self.clips[self.pagina] == True:

            posGeof1 = float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])

            for j in range(self.canais):

                self.plotArts[self.pagina][j].get_xdata()[self.plotArts[self.pagina][j].get_xdata() < posGeof1+j*self.valordx-((self.valordx/2)*0.9)] = posGeof1+j*self.valordx-((self.valordx/2)*0.9)
                self.plotArts[self.pagina][j].get_xdata()[self.plotArts[self.pagina][j].get_xdata() > posGeof1+j*self.valordx+((self.valordx/2)*0.9)] = posGeof1+j*self.valordx+((self.valordx/2)*0.9)
                self.plotArts[self.pagina][j].set_xdata(self.plotArts[self.pagina][j].get_xdata())

        else:

            pass
         
        if self.sombreamentos[self.pagina] == True:

            for j in range(self.canais):
                
                self.sombArts[self.pagina][:].pop(j).remove()
                
            del self.sombArts[self.pagina][:]

            self.sombreamentos[self.pagina] = False
            self.fill()

        else:

            pass

        self.figs[self.pagina].canvas.draw()
        self.status.configure(text=' ')

        if self.pickMode == True:

            self.status.configure(text=' Pick ativado',fg='blue')

        else:

            pass

    def conferidorGeral(self):

        for i in range(len(self.arquivos)):

            posGeof1 = float(self.sts[i][0].stats.seg2['RECEIVER_LOCATION'])
                
            if self.clips[i] == True:
                    
                for j in range(self.canais):

                    self.plotArts[i][j].get_xdata()[self.plotArts[i][j].get_xdata() < posGeof1+j*self.valordx-((self.valordx/2)*0.9)] = posGeof1+j*self.valordx-((self.valordx/2)*0.9)
                    self.plotArts[i][j].get_xdata()[self.plotArts[i][j].get_xdata() > posGeof1+j*self.valordx+((self.valordx/2)*0.9)] = posGeof1+j*self.valordx+((self.valordx/2)*0.9)
                    self.plotArts[self.pagina][j].set_xdata(self.plotArts[self.pagina][j].get_xdata())

            if self.sombreamentos[i] == False:

                pass
                        
            else:

                for j in range(self.canais):
            
                    self.sombArts[i][:].pop(j).remove()
        
                del self.sombArts[i][:]

                if self.ladoFill == 'positivo':

                    for j in range(self.canais):
            
                        somb = self.axes[i].fill_betweenx(self.plotArts[i][j].get_ydata(),
                                         posGeof1+j*self.valordx,self.plotArts[i][j].get_xdata(),
                                        where=self.plotArts[i][j].get_xdata()>=  posGeof1+j*self.valordx,color='black')

                        self.sombArts[i].append(somb)

                elif self.ladoFill == 'negativo':

                    for j in range(self.canais):
            
                        somb = self.axes[i].fill_betweenx(self.plotArts[i][j].get_ydata(),
                                         posGeof1+j*self.valordx,self.plotArts[i][j].get_xdata(),
                                        where=self.plotArts[i][j].get_xdata()<= posGeof1+j*self.valordx,color='black')

                        self.sombArts[i].append(somb)

            self.telas[i].show()
            
        self.status.configure(text=' ')

        if self.pickMode == True:

            self.status.configure(text=' Pick ativado',fg='blue')

        else:

            pass

    def ampup(self):

        if self.plotExiste == True:

            self.status.configure(text=' Aplicando ganho...')

            self.ganho[self.pagina] += self.valorGanho

            if self.normalizado == True:

                if self.filtros[self.pagina] != True:

                    for j in range(self.canais):
                        
                        self.plotArts[self.pagina][j].set_xdata(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                else:

                    for j in range(self.canais):
                        
                        self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)
                
            else:

                if self.filtros[self.pagina] != True:
                
                    for j in range(self.canais):

                        self.plotArts[self.pagina][j].set_xdata(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                else:

                    for j in range(self.canais):
                        
                        self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

            self.conferidorIndividual()
            
        else:

            pass

    def ampdown(self):

        if self.plotExiste == True and self.ganho[self.pagina] > self.valorGanho:

            self.status.configure(text=' Removendo ganho...')

            self.ganho[self.pagina] -= self.valorGanho

            if self.normalizado == True:

                if self.filtros[self.pagina] != True:

                    for j in range(self.canais):
                        
                        self.plotArts[self.pagina][j].set_xdata(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                else:

                    for j in range(self.canais):
                        
                        self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)
                    
            else:

                if self.filtros[self.pagina] != True:

                    for j in range(self.canais):

                        self.plotArts[self.pagina][j].set_xdata(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                else:

                    for j in range(self.canais):

                        self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

            self.conferidorIndividual()
        
        else:

            pass

    def amostrasDefault(self):

        if self.plotExiste == True:

            if int(self.ndados[self.pagina]) != int(len(self.sts[0][0])):
                
                if messagebox.askyesno('Geosis - Sispick', 'Atualizar os plots para número de amostras original (%d)?'%int(len(self.sts[0][0]))):

                    self.ndados[self.pagina] = int(len(self.sts[0][0]))

                    if self.normalizado == True:

                        for j in range(self.canais):

                            self.plotArts[self.pagina][j].set_data(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx,
                                                         [self.sts[self.pagina][0].stats.delta*k for k in range(int(self.ndados[self.pagina]))])

                    else:

                        for j in range(self.canais):
                    
                            self.plotArts[self.pagina][j].set_data(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx,
                                                         [self.sts[self.pagina][0].stats.delta*k for k in range(int(self.ndados[self.pagina]))])

                    self.axes[self.pagina].set_ylim([0,self.sts[self.pagina][0].stats.delta*self.ndados[self.pagina]])

                    if self.yinvertido == True:
                        
                        plt.figure(self.pagina)
                        plt.gca().invert_yaxis()
                        self.figs[self.pagina].canvas.draw()

                    else:

                        pass

                    self.conferidorIndividual()

                else:

                    pass

        else:

            pass
                    
    def menosy(self):

        if self.plotExiste == True:

            if self.yinvertido == True:

                self.axes[self.pagina].set_ylim([0,float(self.axes[self.pagina].get_ylim()[0])*self.fatorY])
                plt.figure(self.pagina)
                plt.gca().invert_yaxis()

            else:

                self.axes[self.pagina].set_ylim([0,float(self.axes[self.pagina].get_ylim()[1])*self.fatorY])
            
            self.figs[self.pagina].canvas.draw()
     
        else:

            pass

    def maisy(self):

        if self.plotExiste == True:

            if self.yinvertido == True:

                self.axes[self.pagina].set_ylim([0,float(self.axes[self.pagina].get_ylim()[0])/self.fatorY])
                plt.figure(self.pagina)
                plt.gca().invert_yaxis()

            else:

                self.axes[self.pagina].set_ylim([0,float(self.axes[self.pagina].get_ylim()[1])/self.fatorY])
            
            self.figs[self.pagina].canvas.draw()

        else:

            pass

    def normalizar(self):

        if self.plotExiste == True:

            if self.normalizado == False:

                self.status.configure(text=' Normalizando traços...')

                for i in range(len(self.arquivos)):

                    if self.filtros[i] != True:

                        for j in range(self.canais):

                            self.plotArts[i][j].set_xdata(self.dadosNorms[i][j][0:self.ndados[i]]*(-1)*self.ganho[i]+float(self.sts[i][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                    else:

                        messagebox.showinfo('','Retire os filtros aplicados no sismograma para normalizar os traços')

                self.normalizado = True

            else:

                self.status.configure(text=' Removendo normalização de traços...')

                for i in range(len(self.arquivos)):

                    if self.filtros[i] != True:
                    
                        for j in range(self.canais):

                            self.plotArts[i][j].set_xdata(self.dadosCrus[i][j][0:self.ndados[i]]*(-1)*self.ganho[i]+float(self.sts[i][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                    else:

                        messagebox.showinfo('','Retire os filtros aplicados no sismograma para desnormalizar os traços')
                        self.status.configure(text=' ')

                self.normalizado = False

            self.conferidorGeral()
            
        else:

            pass

    def fill(self):
                
        if self.plotExiste == True and self.sombreamentos[self.pagina] == False:

            self.status.configure(text=' Aplicando sombreamento...')

            if self.ladoFill == 'positivo':

                for j in range(self.canais):
                    
                    somb = self.axes[self.pagina].fill_betweenx(self.plotArts[self.pagina][j].get_ydata(),
                                float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+self.valordx*j,
                                self.plotArts[self.pagina][j].get_xdata(),
                                where = self.plotArts[self.pagina][j].get_xdata() >= float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx,color='black')
                        
                    self.sombArts[self.pagina].append(somb)

            elif self.ladoFill == 'negativo':

                for j in range(self.canais):
                    
                    somb = self.axes[self.pagina].fill_betweenx(self.plotArts[self.pagina][j].get_ydata(),
                            float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx,
                            self.plotArts[self.pagina][j].get_xdata(),
                            where = self.plotArts[self.pagina][j].get_xdata() <= float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx,color='black')
                        
                    self.sombArts[self.pagina].append(somb)

            self.figs[self.pagina].canvas.draw()
            self.status.configure(text=' ')
                
            self.sombreamentos[self.pagina]=True

            if self.pickMode == True:

                self.status.configure(text=' Pick ativado',fg='blue')

            else:

                pass

        elif self.plotExiste == True and self.sombreamentos[self.pagina] == True:

            self.status.configure(text=' Removendo sombreamento...')

            for j in range(self.canais):

                self.sombArts[self.pagina][:].pop(j).remove()
                
            del self.sombArts[self.pagina][:]
            self.figs[self.pagina].canvas.draw()
            self.status.configure(text=' ')

            self.sombreamentos[self.pagina]=False

            if self.pickMode == True:

                self.status.configure(text=' Pick ativado',fg='blue')

            else:

                pass

        else:

            pass

    def clip(self):

        if self.plotExiste == True:

            if self.clips[self.pagina] == False:

                self.status.configure(text=' Clipando traços...')
                posGeof1 = float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])

                for j in range(self.canais):

                    self.plotArts[self.pagina][j].get_xdata()[self.plotArts[self.pagina][j].get_xdata() < posGeof1+j*self.valordx-((self.valordx/2)*0.9)] = posGeof1+j*self.valordx-((self.valordx/2)*0.9)
                    self.plotArts[self.pagina][j].get_xdata()[self.plotArts[self.pagina][j].get_xdata() > posGeof1+j*self.valordx+((self.valordx/2)*0.9)] = posGeof1+j*self.valordx+((self.valordx/2)*0.9)
                    self.plotArts[self.pagina][j].set_xdata(self.plotArts[self.pagina][j].get_xdata())

                self.clips[self.pagina] = True

            else:

                self.status.configure(text=' Removendo clip de traços...')

                if self.normalizado == True:

                    for j in range(self.canais):

                        self.plotArts[self.pagina][j].set_xdata(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                else:

                    for j in range(self.canais):

                        self.plotArts[self.pagina][j].set_xdata(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                self.clips[self.pagina] = False
                
            if self.sombreamentos[self.pagina] == True:

                for j in range(self.canais):
                    
                    self.sombArts[self.pagina][:].pop(j).remove()
                    
                del self.sombArts[self.pagina][:]

                self.sombreamentos[self.pagina] = False
                self.fill()

            else:

                pass

            self.figs[self.pagina].canvas.draw()
            self.status.configure(text=' ')

            if self.pickMode == True:

                self.status.configure(text=' Pick ativado',fg='blue')

            else:

                pass

        else:

            pass
  
    def invert(self):

        if self.plotExiste == True:

            if self.yinvertido == False:

                for i in range(len(self.arquivos)):
                    
                    plt.figure(i)
                    plt.gca().invert_yaxis()
                    self.figs[i].canvas.draw()

                self.yinvertido = True

            elif self.yinvertido == True:

                for i in range(len(self.arquivos)):
                    
                    plt.figure(i)
                    plt.gca().invert_yaxis()
                    self.figs[i].canvas.draw()

                self.yinvertido = False

        else:

            pass

    def removerFiltros(self):

        if self.plotExiste == True:

            if self.filtros[self.pagina] == True:

                if self.normalizado == True:

                    for j in range(self.canais):

                        self.plotArts[self.pagina][j].set_xdata(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                    self.copiasNorms[self.pagina] = None

                else:

                    for j in range(self.canais):

                        self.plotArts[self.pagina][j].set_xdata(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

                    self.copiasCruas[self.pagina] = None

                self.statusPA.configure(text = '')
                self.statusPB.configure(text = '')
                self.filtros[self.pagina] = False
                self.filtrosHP[self.pagina] = False
                self.filtrosLP[self.pagina] = False
                self.freqLP[self.pagina] = 1000
                self.freqHP[self.pagina] = 5
                self.conferidorIndividual()
                self.telas[self.pagina].show()

            else:

                pass        

        else:

            pass

    def filtroLP(self):

        if self.plotExiste == True:

            if self.normalizado == True:

                if self.filtros[self.pagina] != True:

                    self.copiasNorms[self.pagina] = self.sts[self.pagina].copy().normalize()
                    self.copiasNorms[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP

                else:

                    self.copiasNorms[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP
                            
                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

            else:

                if self.filtros[self.pagina] != True:

                    self.copiasCruas[self.pagina] = self.sts[self.pagina].copy().normalize(1)
                    self.copiasCruas[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP

                else:

                    self.copiasCruas[self.pagina].filter("lowpass", freq = self.freqLP[self.pagina])
                    self.statusPB.configure(text = 'Passa baixa: %.2f Hz'%self.freqLP[self.pagina])
                    self.freqLP[self.pagina] = self.freqLP[self.pagina]*self.fatorLP
                            
                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

            self.filtrosLP[self.pagina] = True        
            self.filtros[self.pagina] = True
            self.conferidorIndividual()
            self.telas[self.pagina].show()

        else:

            pass

    def filtroHP(self):

        if self.plotExiste == True:

            if self.normalizado == True:

                if self.filtros[self.pagina] != True:

                    self.copiasNorms[self.pagina] = self.sts[self.pagina].copy().normalize()
                    self.copiasNorms[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'Passa alta: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP[self.pagina] = self.freqHP[self.pagina]*self.fatorHP

                else:

                    self.copiasNorms[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'Passa alta: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP[self.pagina] = self.freqHP[self.pagina]*self.fatorHP
                            
                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata(self.copiasNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

            else:

                if self.filtros[self.pagina] != True:

                    self.copiasCruas[self.pagina] = self.sts[self.pagina].copy().normalize(1)
                    self.copiasCruas[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'Passa alta: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP[self.pagina] = self.freqHP[self.pagina]*self.fatorHP

                else:

                    self.copiasCruas[self.pagina].filter("highpass", freq = self.freqHP[self.pagina])
                    self.statusPA.configure(text = 'Passa alta: %.2f Hz'%self.freqHP[self.pagina])
                    self.freqHP = self.freqHP[self.pagina]*self.fatorHP
                            
                for j in range(self.canais):

                    self.plotArts[self.pagina][j].set_xdata(self.copiasCruas[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx)

            self.filtrosHP[self.pagina] = True
            self.filtros[self.pagina] = True
            self.conferidorIndividual()
            self.telas[self.pagina].show()

        else:

            pass

    def salvargp(self):

        if not self.picks[:]:

            messagebox.showerror('Geosis - Sispick','Nao há picks')
            
        else:
            
            try:
                
                arquivoSaida = filedialog.asksaveasfilename(title='Salvar',filetypes=[('Geosis pick', '.gp')])
                
                with open(arquivoSaida+'.gp','a') as arqpck:

                    for i in range(len(self.arquivos)):
                            
                        for key in sorted(self.picks[i]):
                            
                            arqpck.write('%f %f 1\n'%(key,self.picks[i][key]*1000))

                        if self.seg2 == True:

                            arqpck.write('/ %f\n'%(float(self.listSource[i])))

                        else:

                            arqpck.write('0.0 %d 0.0\n'%self.canais)

                arqpck.close()
                messagebox.showinfo('Geosis - Sispick','Pick salvo')

            except:

                pass

    def salvarpick(self):

        if not self.picks[:]:

            messagebox.showerror('Geosis - Sispick','Nao há picks')
            
        else:
            
            try:
                
                arquivoSaida = filedialog.asksaveasfilename(title='Salvar',filetypes=[('Seisimager', '.vs')])
                
                with open(arquivoSaida+'.vs','a') as arqpck:

                    arqpck.write('1996 0 3.0\n0 %d %f\n'%(len(self.arquivos),self.valordx))

                    for i in range(len(self.arquivos)):

                        if self.seg2 == True:

                            arqpck.write('%f %d 0.0\n'%(float(self.listSource[i]), self.canais))

                        else:

                            arqpck.write('0.0 %d 0.0\n'%self.canais)
                            
                        for key in sorted(self.picks[i]):
                            
                            arqpck.write('%f %f 1 \n'%(key,self.picks[i][key]*1000))

                    arqpck.write('0 0 \n 0 \n 0 0 \n')

                arqpck.close()
                messagebox.showinfo('Geosis - Sispick','Pick salvo')

            except:

                pass

    def pickAmostra(self):

        if self.plotExiste == True:

            def pick(event):

                if int(event.ydata/self.sts[0][0].stats.delta) <= int(len(self.sts[0][0])):

                    marcador = self.axes[self.pagina].hlines(event.ydata,float(self.axes[0].get_xlim()[0]),
                                            float(self.axes[0].get_xlim()[1]),colors='r',linestyle='--',
                                            alpha = 1,linewidth = 2)
                    self.figs[self.pagina].canvas.draw()
                
                    if messagebox.askyesno('Geosis - Sispick', 'Atualizar os plots para %d amostras?'%int(event.ydata/self.sts[0][0].stats.delta)):

                        marcador.remove()
                        self.ndados[self.pagina] = int(event.ydata/self.sts[0][0].stats.delta)

                        if self.normalizado == True:

                            for j in range(self.canais):

                                self.plotArts[self.pagina][j].set_data(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx,
                                                             [self.sts[self.pagina][0].stats.delta*k for k in range(int(self.ndados[self.pagina]))])

                        else:

                            for j in range(self.canais):
                        
                                self.plotArts[self.pagina][j].set_data(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx,
                                                             [self.sts[self.pagina][0].stats.delta*k for k in range(int(self.ndados[self.pagina]))])

                        self.axes[self.pagina].set_ylim([0,self.sts[self.pagina][0].stats.delta*self.ndados[self.pagina]])

                        if self.yinvertido == True:
                            
                            plt.figure(self.pagina)
                            plt.gca().invert_yaxis()
                            self.figs[self.pagina].canvas.draw()

                        else:

                            pass

                        self.figs[self.pagina].canvas.mpl_disconnect(self.cid)
                        self.pickAmostraAtivado = False

                        self.status.configure(text='',fg='red')      
                        self.conferidorIndividual()
                        
                    else:
                            
                        self.figs[self.pagina].canvas.mpl_disconnect(self.cid)
                        self.status.configure(text='',fg='red')
                        self.pickAmostraAtivado = False
                        marcador.remove()

            if self.pickAmostraAtivado == False:

                self.cid = self.figs[self.pagina].canvas.mpl_connect('button_press_event', pick)
                self.status.configure(text='Editor de amostras ON', fg='blue')                    
                self.pickAmostraAtivado = True

            else:

                self.figs[self.pagina].canvas.mpl_disconnect(self.cid)
                self.status.configure(text='', fg='red')
                self.pickAmostraAtivado = False
                    
        else:

            pass

    def cabecalho (self):

        if self.plotExiste == True:

            root = Tk()
            root.geometry('430x300')
            root.title('Geosis - Sispick')
            root.resizable(0,0)
            fonte = StringVar()
            dx = StringVar()
            comp = StringVar()
            pts = StringVar()
            main = Label(root, text = 'Dados do cabeçalho (%s)'%os.path.basename(self.arquivos[self.pagina]),font=("Helvetica", 14),
                         fg='green').grid(row = 0, column = 0, sticky='w', padx = 10, pady = 10)
            fonte = Label(root, text = 'Posição da fonte (atual: %.1f m):'%float(self.listSource[self.pagina]),font=("Helvetica", 12),
                         fg='black').grid(row = 1, column = 0, sticky='w', padx = 10, pady = 10)
            espacamento = Label(root, text = 'Espaçamento entre geofones (atual: %.1f m):'%float(self.valordx),font=("Helvetica", 12),
                         fg='black').grid(row = 2, column = 0, sticky='w', padx = 10, pady = 10)
            comp = Label(root, text = 'Comprimento do perfil (atual: %.1f m):'%(float(self.sts[self.pagina][-1].stats.seg2['RECEIVER_LOCATION'])-float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])),font=("Helvetica", 12),
                         fg='black').grid(row = 3, column = 0, sticky='w', padx = 10, pady = 10)
            pontos = Label(root, text = 'Quantidade de amostras (atual: %d):'%int(self.ndados[self.pagina]),font=("Helvetica", 12),
                         fg='black').grid(row = 4, column = 0, sticky='w', padx = 10, pady = 10)
            entryf = Entry(root, textvariable = fonte, width=10)
            entryf.grid(row = 1, column = 0, sticky = 'w', pady = 10, padx = 250)
            entrydx = Entry(root, textvariable = dx, width=10)
            entrydx.grid(row = 2, column = 0, sticky = 'w', pady = 10, padx = 330)
            entrycomp = Entry(root, textvariable = comp, width=10)
            entrycomp.grid(row = 3, column = 0, sticky = 'w', pady = 10, padx = 290)
            entrypontos = Entry(root, textvariable = pts, width=10)
            entrypontos.grid(row = 4, column = 0, sticky = 'w', pady = 10, padx = 290)
            warning = Label(root, text = ' ', fg = 'red',font=("Helvetica", 12))
            warning.grid(row = 6, column = 0, sticky = 'w', padx = 100, pady= 10)
            
            def salvar():

                if len(entryf.get()) > 0:
                    
                    try:

                        self.listSource[self.pagina] = float(entryf.get())
                        warning.configure(text = 'Dados salvos', fg = 'blue')
                        
                    except:

                        warning.configure(text = 'Posição de fonte inválida', fg = 'red')

                else:

                    pass

                if len(entrydx.get()) > 0:
                    
                    try:

                        self.valordx = float(entrydx.get())
                        warning.configure(text = 'Dados salvos', fg = 'blue')

                        for i in range(len(self.arquivos)):

                            if self.normalizado == True:

                                for j in range(self.canais):
                        
                                    self.plotArts[i][j].set_xdata([self.stsNorms[i][j][k]*(-1)*self.ganho[i]+j*self.valordx for k in range(self.ndados[i])])

                            else:

                                for j in range(self.canais):
                        
                                    self.plotArts[i][j].set_xdata([self.sts[i][j][k]*(-1)*self.ganho[i]+j*self.valordx for k in range(self.ndados[i])])
                
                            self.conferidorGeral()
                            
                    except:

                        warning.configure(text = 'Espaçamento entre geofones inválido', fg = 'red')

                if len(entrycomp.get()) > 0:
                    
                    try:

                        warning.configure(text = 'Dados salvos', fg = 'blue')

                        for i in range(len(self.arquivos)):

                            plt.figure(i)
                            plt.xlim(float(self.sts[i][0].stats.seg2['RECEIVER_LOCATION'])-self.valordx,float(entrycomp.get())+self.valordx)
                            self.telas[i].show()
                            
                    except:

                        warning.configure(text = 'Comprimento de perfil inválido', fg = 'red')

                if len(entrypontos.get()) > 0 and int(entrypontos.get()) <= len(self.sts[self.pagina][0]):

                    self.ndados[self.pagina] = int(entrypontos.get())

                    if self.normalizado == True:

                        for j in range(self.canais):

                            self.plotArts[self.pagina][j].set_data(self.dadosNorms[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx,
                                                         [self.sts[self.pagina][0].stats.delta*k for k in range(int(self.ndados[self.pagina]))])

                    else:

                        for j in range(self.canais):
                    
                            self.plotArts[self.pagina][j].set_data(self.dadosCrus[self.pagina][j][0:self.ndados[self.pagina]]*(-1)*self.ganho[self.pagina]+float(self.sts[self.pagina][0].stats.seg2['RECEIVER_LOCATION'])+j*self.valordx,
                                                         [self.sts[self.pagina][0].stats.delta*k for k in range(int(self.ndados[self.pagina]))])

                    self.axes[self.pagina].set_ylim([0,self.sts[self.pagina][0].stats.delta*self.ndados[self.pagina]])

                    if self.yinvertido == True:
                        
                        plt.figure(self.pagina)
                        plt.gca().invert_yaxis()
                        self.figs[self.pagina].canvas.draw()

                    else:

                        pass
                        
                    self.telas[self.pagina].show()
                    self.conferidorIndividual()

                else:

                    pass

            def fechar():

                root.destroy()

            save = Button(root, text = 'Salvar',font=("Helvetica", 12), width = 6,
                    command = salvar).grid(row = 5, column = 0, sticky = 'w', padx = 80, pady = 10)
            fechar = Button(root, text = 'Fechar',font=("Helvetica", 12), width = 6,
                    command = fechar).grid(row = 5, column = 0, sticky = 'w', padx = 220, pady = 10)
            root.mainloop()

        else:

            pass

    def configPlot(self):

        if self.plotExiste == True and self.optAberto == False:

            root = Tk()
            root.geometry('420x350+500+250')
            root.title('Sismograma')
            vardx = StringVar()
            varY = StringVar()
            varGain = StringVar()    
            varFigx = StringVar()
            varFigy = StringVar()
            mainLabel = Label(root, text='Configurações de plot',
                        font=("Helvetica", 14),fg='green').grid(row=0, column=0, sticky="w",pady=15,padx=110)
            labelY = Label(root, text='Corte temporal (atual: %.1f s): '%self.fatorY,
                           font=("Helvetica", 12)).grid(row=1, column=0, sticky="w",padx=20,pady=10)
            entryY = Entry(root, textvariable = varY,width=10)
            entryY.grid(row=1, column=0, sticky="w",padx=235,pady=10)
            labelGain = Label(root, text='Fator de ganho (atual: %.1f): '%self.valorGanho,
                              font=("Helvetica", 12)).grid(row=2, column=0, sticky="w",padx=20,pady=10)
            entryGain = Entry(root, textvariable = varGain,width=10)
            entryGain.grid(row=2, column=0, sticky="w",padx=235,pady=10)
            labelFigx = Label(root, text='Tamanho x do plot (atual: %.1f): '%self.valorFigx,
                              font=("Helvetica", 12)).grid(row=3, column=0, sticky="w",padx=20,pady=10)
            entryFigx = Entry(root, textvariable = varFigx,width=10)
            entryFigx.grid(row=3, column=0, sticky="w",padx=235,pady=10)
            labelFigy = Label(root, text='Tamanho y do plot (atual: %.1f): '%self.valorFigy,
                              font=("Helvetica", 12)).grid(row=4, column=0, sticky="w",padx=20,pady=10)
            entryFigy = Entry(root, textvariable = varFigy,width=10)
            entryFigy.grid(row=4, column=0, sticky="w",padx=235,pady=10)

            fill = Label(root, text='Lado do sombreamento (atual: %s): '%self.ladoFill,
                              font=("Helvetica", 12)).grid(row=5, column=0, sticky="w",padx=20,pady=10)
            warning = Label(root, text='',font=("Helvetica", 12),fg = 'red')
            warning.grid(row=7, column=0, sticky="w",pady=0,padx=140)

            def fechar():

                self.optAberto = False
                root.destroy()
                
            def do():

                if len(entryY.get()) > 0:

                    try:

                        self.fatorY = float(entryY.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')

                    except:

                        warning.configure(text='Corte temporal inválido',fg = 'red')

                if len(entryGain.get()) > 0:

                    try:

                        self.valorGanho = float(entryGain.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')

                    except:

                        warning.configure(text='Fator de ganho inválido',fg = 'red')

                if len(entryFigx.get()) > 0:

                    try:

                        self.valorFigx = float(entryFigx.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')

                        for i in range(len(self.arquivos)):

                            plt.figure(i)
                            plt.gcf().set_size_inches(self.valorFigx, self.valorFigy,forward=True)
                            self.figs[i].canvas.draw()

                    except:

                        warning.configure(text='Tamanho x inválido',fg = 'red')

                if len(entryFigy.get()) > 0:

                    try:

                        self.valorFigy = float(entryFigy.get())
                        warning.configure(text='Configurações aplicadas',fg = 'blue')

                        for i in range(len(self.arquivos)):

                            plt.figure(i)
                            plt.gcf().set_size_inches(self.valorFigx, self.valorFigy,forward=True)
                            self.figs[i].canvas.draw()

                    except:

                         warning.configure(text='Tamanho y inválido',fg = 'red')

            def cancelar():

                self.optAberto = False
                root.destroy()

            def negativo():

                self.ladoFill = 'negativo'

            def positivo():

                self.ladoFill = 'positivo'

            neg = Button(root, text=' - ',width=4,
                         command = negativo).grid(row=5, column=0, sticky="w",padx=310,pady=10)
            pos = Button(root, text=' + ',width=4,
                         command = positivo).grid(row=5, column=0, sticky="w",padx=360,pady=10)
            botaoOK = Button(root, text='Aplicar', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black',width=8, command = do).grid(row=6, column=0, sticky="w",pady=20,padx=110)
            botaoX = Button(root, text='Fechar', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black',width=8, command = cancelar).grid(row=6, column=0, sticky="w",padx=260,pady=20)
            root.bind('<Return>', lambda x: do())
            root.resizable(0,0)
            root.protocol("WM_DELETE_WINDOW", fechar)
            self.optAberto = True
            root.mainloop()

        elif self.plotExiste == True and self.optAberto == True:

            pass

        else:

            pass

    def configDx(self):                 
        
        root = Tk()   
        root.geometry('455x230+500+250')
        root.title('Geosis - Sispick')
        vardx = StringVar()
        mainLabel = Label(root, text='O espaçamento entre geofones não foi encontrado no cabeçalho\ndo arquivo. Insira manualmente no campo abaixo',
                    font=("Helvetica", 11),fg='red').grid(row=0, column=0, sticky="w",pady=15,padx=5)
        labeldx = Label(root, text='Espaçamento entre geofones (metros): ',
                    font=("Helvetica", 12)).grid(row=2, column=0, sticky="w",padx=20,pady=10)
        entrydx = Entry(root, textvariable = vardx,width=10)
        entrydx.grid(row=2, column=0, sticky="w",padx=310,pady=10)
        warning = Label(root, text = '', fg = 'red',font=("Helvetica", 12))
        warning.grid(row = 6, column = 0, sticky = 'w', pady = 5, padx = 180)
        
        def do():
            
            if len(entrydx.get()) > 0:

                try:
                
                    self.valordx = float(entrydx.get())
                    root.destroy()
                    self.abrir_pt2()

                except:
                    
                    warning.configure(text = 'Valor inválido')

            else:

                messagebox.showinfo('Geosis - Sispick', 'Espaçamento entre geofones padrão será usado: 2 m')
                self.valordx = 2
                root.destroy()
                self.abrir_pt2()
                                    
        def cancelar():

            messagebox.showinfo('Geosis - Sispick', 'Espaçamento entre geofones padrão será usado: 2 m')
            self.valordx = 2
            root.destroy()
            self.abrir_pt2()
        
        botaoOK = Button(root, text='   Ok   ', bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',width=8, command = do).grid(row=5, column=0, sticky="w",pady=20,padx=110)
        botaoX = Button(root, text='Ignorar', bg = 'gray90',fg='black', activebackground = 'gray93',
                        activeforeground = 'black',width=8, command = cancelar).grid(row=5, column=0, sticky="w",padx=260,pady=20)
        entrydx.focus()
        root.bind('<Return>', lambda x: do())
        root.resizable(0,0)
        root.protocol("WM_DELETE_WINDOW", cancelar)
        root.mainloop()


class sisref(Tk):

    def __init__(self):

        Tk.__init__(self)
        self.configure(background='#F3F3F3')
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(),
                                       self.winfo_screenheight()))        
        self.title('Geosis - sisref')
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        parent = Frame(self,bg='#F3F3F3')
        parent.grid(row=0,column=0,sticky='nsew')
        barraDEmenu = Menu(self)
        self.configure(menu=barraDEmenu)
        menu_arquivo=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Arquivo',menu=menu_arquivo)
        menu_arquivo.add_command(label='Abrir arquivo tempo de percurso (.gp)                    Ctrl+A',
                                      command=self.abrirgp)
        menu_curva=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Curvas',menu=menu_curva)
        menu_curva.add_command(label='Editar curvas                    Ctrl+E',
                                      command=self.editarCurva)
        menu_inversao=Menu(barraDEmenu)
        barraDEmenu.add_cascade(label='Inversão',menu=menu_inversao)
        menu_inversao.add_command(label='Atribuir camada 2                    Ctrl+E',
                                      command=self.camadas)
        menu_inversao.add_command(label='Atribuir camada 3                    Ctrl+E',
                                      command=self.camadas)
        menu_inversao.add_command(label='Calcular velocidades                    Ctrl+E',
                                      command=self.velocidades)
        botao_editor = Button(parent, text='E',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                              bg = 'floral white',activeforeground='black',
                         activebackground = 'snow', command = self.editarCurva).grid(row=0,column=2,sticky=W)
        botao_c2 = Button(parent, text='C',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                              bg = 'red',activeforeground='white',
                         activebackground = 'orange red', command = self.camadas).grid(row=0,column=3,sticky=W)
        botao_v = Button(parent, text='V',fg= 'black',font=("Arial", 10,'bold'),width = 4,
                              bg = 'dodger blue',activeforeground='white',
                         activebackground = 'sky blue', command = self.velocidades).grid(row=0,column=4,sticky=W)
        self.status = Label(parent,text = '', fg='green',font=("Helvetica", 12))
        self.status.grid(row=0,column=13,sticky=E)
        self.frame = Frame(self,bg='#F3F3F3')
        self.frame.grid(row=1, column=0,sticky='nsew')

        self.xData = {}
        self.yData = {}
        self.linhas = []
        self.fontes = {}
        self.bolas = {}
        self.camadas = {}
        self.xDataCamada1 = {}
        self.yDataCamada1 = {}
        self.xDataCamada2 = {}
        self.yDataCamada2 = {}
        self.sublinhas = {}
        self.especiais = {}
        self.cores = {}
        self.retas = {}
        self.retas2 = {}
        self.temp = []
        self.temp2 = []
        self.vels = []
        self.vels2 = []
        self.nlinhas = 0
        self.count = 1
        self.count2 = 0
        self.sublinha = 0
        self.linha = None
        self.cor = None
        self.artista = None

        self.valorFigx = self.winfo_screenwidth()/161

        if self.winfo_screenheight() == 1080:
            
            self.valorFigy = self.winfo_screenheight()/93.10

        elif self.winfo_screenheight() == 768:

            self.valorFigy = self.winfo_screenheight()/99.74

        elif self.winfo_screenheight() == 1024:

            self.valorFigy = self.winfo_screenheight()/94.1

        elif self.winfo_screenheight() == 900:

            self.valorFigy = self.winfo_screenheight()/96.5

        elif self.winfo_screenheight() == 720:

            self.valorFigy = self.winfo_screenheight()/101.5

        else: # 800

            self.valorFigy = self.winfo_screenheight()/99

        plt.rcParams['keymap.zoom'] = 'z,Z'
        plt.rcParams['keymap.back'] = 'v,V'
        plt.rcParams['keymap.home'] = 'ctrl+z,ctrl+Z'
        plt.rcParams['keymap.save'] = 'ctrl+i,ctrl+I'
        plt.rcParams['keymap.pan'] = 'm,M'
        self.bind('<Control-a>', lambda x: self.abrirgp())
        self.bind('<Control-A>', lambda x: self.abrirgp())

        self.curvaExiste = False
        
        self.mainloop()

    def fechar(self):

        if messagebox.askyesno("Geosis - sisref", "Sair do programa?"):

            self.destroy()

        else:

            pass

    def abrirgp(self):

        if self.curvaExiste == True:

            messagebox.showinfo('','Feche a curva atual antes de abrir uma nova')

        else:

            try:

                arquivo = filedialog.askopenfilename(title='Abrir',filetypes=[('Geosis pick','*.gp'),
                                                                    ('Todos os arquivos','*.*')])
            except:

                pass

            if len(arquivo) > 0:
            
                dados = open(arquivo).readlines()
                
                linhas = [i.strip('\n') for i in dados]

                for i in linhas:

                    if i.split()[0] != '/':

                        self.temp.append(float(i.split()[0]))

                    else:
                        
                        self.nlinhas += 1
                        self.fontes.update({self.nlinhas:float(i.split()[1])})
                        
                        if self.temp[0] < float(i.split()[1]) and self.temp[-1] > float(i.split()[1]):

                            self.especiais[self.nlinhas] = float(i.split()[1])

                            del self.temp[:]

                for i in range(self.nlinhas):

                    if i+1 in self.especiais:

                        self.xData[i+1] = []
                        self.yData[i+1] = []
                        self.xDataCamada1[i+1] = {}
                        self.yDataCamada1[i+1] = {}
                        self.xDataCamada2[i+1] = {}
                        self.yDataCamada2[i+1] = {}

                        for j in range(2):

                            self.xDataCamada1[i+1][j+1] = []
                            self.yDataCamada1[i+1][j+1] = []
                            self.xDataCamada2[i+1][j+1] = []
                            self.yDataCamada2[i+1][j+1] = []
                            
                    else:
                        
                        self.xData[i+1] = []
                        self.yData[i+1] = []
                        self.xDataCamada1[i+1] = []
                        self.yDataCamada1[i+1] = []
                        self.xDataCamada2[i+1] = []
                        self.yDataCamada2[i+1] = []

                for i in linhas:

                    if i.split()[0] != '/':                       

                        self.xData[self.count].append(float(i.split()[0]))
                        self.yData[self.count].append(float(i.split()[1]))

                    else:

                        self.count += 1

                self.fig = plt.figure(figsize=(self.valorFigx,self.valorFigy),facecolor='#F3F3F3')
                self.ax = self.fig.add_subplot(111)
                
                for i in range(self.nlinhas):

                    linha, = self.ax.plot(self.xData[i+1],self.yData[i+1], picker = 0, color='black')
                    self.linhas.append(linha,)
                    self.ax.scatter(float(self.fontes[i+1]),0,s=80,alpha=1,marker=(5,1),color='#E5C100')
                    #self.ax.axvline(float(self.fontes[i+1]),color='black',linestyle='--')
                    self.bolas[i+1] = []

                    if self.fontes[i+1] > float(self.xData[i+1][-1]):

                        for j,k in zip(self.xData[i+1][::-1],self.yData[i+1][::-1]):

                            bola = self.ax.scatter(j, k, s=30,c = 'white', alpha=1, picker = 5)
                            self.bolas[i+1].append(bola)
                            self.camadas[bola] = 1
                            self.cores[bola] = 'white'

                    elif i+1 in self.especiais:

                        for j in self.xData[i+1]:

                            if float(j) < self.fontes[i+1]:
                            
                                self.temp2.append(j)
                                self.count2 += 1

                        for j,k in zip(self.temp2[::-1],range(self.count2-1,-1,-1)):

                            bola = self.ax.scatter(j, self.yData[i+1][k], s=30,c = 'white', alpha=1, picker = 5)
                            self.bolas[i+1].append(bola)
                            self.camadas[bola] = 1
                            self.sublinhas[bola] = 1
                            self.cores[bola] = 'white'

                        del self.temp2[:]
                        self.count2 = 0

                        for j in self.xData[i+1]:

                            if float(j) > self.fontes[i+1]:
                            
                                self.temp2.append(j)
                                self.count2 += 1

                        restantes = len(self.xData[i+1])-self.count2

                        for j,k in zip(self.temp2,range(restantes,len(self.xData[i+1]),1)):

                            bola = self.ax.scatter(j, self.yData[i+1][k], s=30,c = 'white', alpha=1, picker = 5)
                            self.bolas[i+1].append(bola)
                            self.camadas[bola] = 1
                            self.sublinhas[bola] = 2
                            self.cores[bola] = 'white'

                        del self.temp2[:]
                        self.count2 = 0

                    else:

                        for j in range(len(self.xData[i+1])):
                                
                            bola = self.ax.scatter(self.xData[i+1][j], self.yData[i+1][j], s=30,c = 'white', alpha=1, picker = 5)
                            self.bolas[i+1].append(bola)
                            self.camadas[bola] = 1
                            self.cores[bola] = 'white'

                plt.title('Curva de tempo de percurso')     
                plt.xlabel('Distância (m)')
                plt.ylabel('Tempo (ms)')
                plt.grid()
                self.ax.xaxis.grid(linestyle='-', linewidth=.4)
                self.ax.yaxis.grid(linestyle='-', linewidth=.4)
                self.tela = FigureCanvasTkAgg(self.fig, self.frame)
                self.tela.show()
                self.tela.get_tk_widget().pack(fill='both', expand=True)
                toolbar = NavigationToolbar2TkAgg(self.tela, self.frame)
                toolbar.update()
                self.tela._tkcanvas.pack(fill='both', expand=True)

                def do(event):
                        
                    key_press_handler(event, self.tela, toolbar)
                    
                self.fig.canvas.mpl_connect('key_press_event', do)
                self.curvaExiste = True
                self.apertado = False
                self.editorOn = False
                self.layerPick = False
                self.status.configure(text = ' Editor de traços: Off   Editor de camadas: Off')
                    
            else:

                pass

    def onoffcheck(self):

        if self.editorOn == True and self.layerPick == True:
                    
            self.status.configure(text = ' Editor de traços: On   Editor de camadas: On')
                    
        elif self.editorOn == True and self.layerPick == False:
            
            self.status.configure(text = ' Editor de traços: On   Editor de camadas: Off')

        elif self.editorOn == False and self.layerPick == True:
            
            self.status.configure(text = ' Editor de traços: Off   Editor de camadas: On')

        else:

            self.status.configure(text = ' Editor de traços: Off   Editor de camadas: Off')

    def editarCurva(self):

        if self.curvaExiste == True:

            if self.editorOn == True:

                self.fig.canvas.mpl_disconnect(self.conexao1)
                self.fig.canvas.mpl_disconnect(self.conexao2)
                self.editorOn = False
                self.onoffcheck()
                
            else:
                    
                def click(event):

                    for i in range(self.nlinhas):

                        if event.artist in self.bolas[i+1]:

                            self.coordy = float(event.artist.get_offsets()[0][1])
                            self.coordx = float(event.artist.get_offsets()[0][0])
                            self.apertado = True
                            self.linha = i+1
                            self.artista = event.artist
                            break
                            
                        else:

                            pass

                def soltar(event):

                    if self.apertado == True:

                        for j in self.xData[self.linha]:

                            if float(j) == self.coordx:
  
                                self.yData[self.linha][self.xData[self.linha].index(self.coordx)] = float(event.ydata)
                                self.bolas[self.linha][self.bolas[self.linha].index(self.artista)].remove()
                                bola = self.ax.scatter(self.coordx,float(event.ydata),
                                                       s=30,c = self.cores[self.artista], alpha=1, picker = 5)
                                self.bolas[self.linha][self.bolas[self.linha].index(self.artista)] = bola

                                for i in self.cores:

                                    if i == self.artista:
                                        
                                        self.cores[bola] = self.cores[i]
                                        del self.cores[i]
                                        break

                                self.linhas[self.linha-1].set_ydata(self.yData[self.linha])
                                self.tela.show()
                                self.apertado = False
                                break
                        
                            else:
    
                                pass
                  
                    else:

                        pass

                self.conexao1 = self.fig.canvas.mpl_connect('pick_event', click)
                self.conexao2 = self.fig.canvas.mpl_connect('button_release_event', soltar)
                self.editorOn = True
                self.onoffcheck()

        else:

            pass

    def camadas(self):

        if self.curvaExiste == True:
        
            if self.layerPick == True:

                self.fig.canvas.mpl_disconnect(self.conexao3)
                self.layerPick = False
                self.onoffcheck()

            else:

                for i in self.cores:

                    if self.cores[i] == 'white':

                        for k in range(self.nlinhas):

                            for j in range(len(self.xData[k+1])):

                                self.bolas[k+1][j].set_color('red')

                            for j in self.bolas[k+1]:

                                if k+1 in self.especiais:

                                    if float(j.get_offsets()[0][0]) < float(self.especiais[k+1]):

                                        self.camadas[j] = 1
                                        self.xDataCamada1[k+1][1].append(float(j.get_offsets()[0][0]))
                                        self.yDataCamada1[k+1][1].append(float(j.get_offsets()[0][1]))

                                    elif float(j.get_offsets()[0][0]) > float(self.especiais[k+1]): 

                                        self.camadas[j] = 1
                                        self.xDataCamada1[k+1][2].append(float(j.get_offsets()[0][0]))
                                        self.yDataCamada1[k+1][2].append(float(j.get_offsets()[0][1]))

                                else:

                                    self.camadas[j] = 1
                                    self.xDataCamada1[k+1].append(float(j.get_offsets()[0][0]))
                                    self.yDataCamada1[k+1].append(float(j.get_offsets()[0][1]))

                        self.cores[i] = 'red'
                        self.tela.show()

                    else:

                        pass

                def click2(event):

                    for i in range(self.nlinhas):

                        if event.artist in self.bolas[i+1]:

                            linha = i+1

                        else:

                            pass
                    
                    if linha in self.especiais:

                        if event.artist in self.sublinhas:

                            self.sublinha = self.sublinhas[event.artist]

                        else:

                            pass

                        if self.sublinha == 1:

                            del self.xDataCamada1[linha][1][:]
                            del self.yDataCamada1[linha][1][:]
                            del self.xDataCamada2[linha][1][:]
                            del self.yDataCamada2[linha][1][:]

                        elif self.sublinha == 2:

                            del self.xDataCamada1[linha][2][:]
                            del self.yDataCamada1[linha][2][:]
                            del self.xDataCamada2[linha][2][:]
                            del self.yDataCamada2[linha][2][:]

                        else:

                            pass

                    else:

                        if len(self.xDataCamada1[linha]) > 0:
                            
                            del self.xDataCamada1[linha][:]
                            del self.yDataCamada1[linha][:]
                            del self.xDataCamada2[linha][:]
                            del self.yDataCamada2[linha][:]

                        else:

                            pass

                    if event.artist in self.bolas[linha]:

                        for bola in self.bolas[linha]:

                            if linha in self.especiais:

                                if float(event.artist.get_offsets()[0][0]) < float(self.especiais[linha]):

                                    if float(bola.get_offsets()[0][1]) >= float(event.artist.get_offsets()[0][1]) and float(bola.get_offsets()[0][0]) < float(self.especiais[linha]):
                
                                        bola.set_color('#1BB270')
                                        self.camadas[event.artist] = 2
                                        self.xDataCamada2[linha][1].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada2[linha][1].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = '#1BB270'
                                                break

                                    elif float(bola.get_offsets()[0][1]) <= float(event.artist.get_offsets()[0][1]) and float(bola.get_offsets()[0][0]) < float(self.especiais[linha]):

                                        bola.set_color('red')
                                        self.camadas[event.artist] = 1
                                        self.xDataCamada1[linha][1].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada1[linha][1].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = 'red'
                                                break
                                    
                                elif float(event.artist.get_offsets()[0][0]) > float(self.especiais[linha]):

                                    if float(bola.get_offsets()[0][1]) >= float(event.artist.get_offsets()[0][1]) and float(bola.get_offsets()[0][0]) > float(self.especiais[linha]):

                                        bola.set_color('#1BB270')
                                        self.camadas[event.artist] = 2                                              
                                        self.xDataCamada2[linha][2].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada2[linha][2].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = '#1BB270'
                                                break
                                        
                                    elif float(bola.get_offsets()[0][1]) <= float(event.artist.get_offsets()[0][1]) and float(bola.get_offsets()[0][0]) > float(self.especiais[linha]):

                                        bola.set_color('red')
                                        self.camadas[event.artist] = 1
                                        self.xDataCamada1[linha][2].append(float(bola.get_offsets()[0][0]))
                                        self.yDataCamada1[linha][2].append(float(bola.get_offsets()[0][1]))

                                        for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = 'red'
                                                break
                                        
                            else:
                                     
                                if float(bola.get_offsets()[0][1]) >= float(event.artist.get_offsets()[0][1]):

                                    bola.set_color('#1BB270')
                                    self.camadas[event.artist] = 2
                                    self.xDataCamada2[linha].append(float(bola.get_offsets()[0][0]))
                                    self.yDataCamada2[linha].append(float(bola.get_offsets()[0][1]))

                                    for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = '#1BB270'
                                                break

                                else:

                                    bola.set_color('red')
                                    self.camadas[event.artist] = 1
                                    self.xDataCamada1[linha].append(float(bola.get_offsets()[0][0]))
                                    self.yDataCamada1[linha].append(float(bola.get_offsets()[0][1]))

                                    for i in self.cores:

                                            if i == bola:

                                                self.cores[i] = 'red'
                                                break
                                 
                        self.tela.show()
                        
                self.conexao3 = self.fig.canvas.mpl_connect('pick_event', click2)
                self.layerPick = True
                self.onoffcheck()

        else:

            pass

    def velocidades(self):

        if len(self.retas) > 0:

            self.retas.clear()
            self.retas2.clear()
            del self.vels[:]
            del self.vels2[:]

        else:

            pass

        for j,k,l,m in zip(self.xDataCamada1.values(),self.yDataCamada1.values(),self.xDataCamada2.values(),self.yDataCamada2.values()):

            if type(j) == dict:

                self.retas.update({str(j[1]):k[1]})
                self.retas.update({str(j[2]):k[2]})
                self.retas2.update({str(l[1]):m[1]})
                self.retas2.update({str(l[2]):m[2]})

            else:

                self.retas.update({str(j):k})
                self.retas2.update({str(l):m})

        self.xretaCamada1 = []
        self.yretaCamada1 = []

        for i in self.retas:

            lista = ast.literal_eval(i)

            for j in lista:
                
                self.xretaCamada1.append(j)

            for j in self.retas[i]:
                    
                self.yretaCamada1.append(j)
                    
        slope, intercept, r_value, p_value, std_err = stats.linregress(sorted(self.xretaCamada1),sorted(self.yretaCamada1))
        print(1/slope)

        for i,j,k,l in zip(self.retas,self.retas.values(),self.retas2,self.retas2.values()):

            slope, intercept, r_value, p_value, std_err = stats.linregress(ast.literal_eval(i),j)
            self.vels.append(abs(1/slope))
            slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(ast.literal_eval(k),l)
            self.vels2.append(abs(1/slope2))

        vmed1 = sum(self.vels) / float(len(self.vels))
        vmed2 = sum(self.vels2) / float(len(self.vels2))
        messagebox.showinfo('','Velocidades médias: camada 1 = %.2f km/s, camada 2 = %.2f km/s'%(vmed1,vmed2))


class Siscon(Tk):
    
    def __init__(self):

        Tk.__init__(self)           
        self.geometry('260x320+600+200')
        self.title('Geosis - Siscon')
        self.formatos = ['SEGY','MSEED']
        self.frame = Frame(self)
        self.nome_formato = StringVar()
        strEntrada = StringVar()
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.labelEntrada = Label(self.frame, text='Arquivos de entrada:',fg='black',font=("Helvetica", 12))
        self.labelSaida = Label(self.frame, text='Diretório de saída:',fg='black',font=("Helvetica", 12))
        self.botaoEntrada = Button(self.frame, text=' ... ', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black', command = self.entrada,width = 4)
        self.botaoSaida = Button(self.frame, text=' ... ', bg = 'gray90',fg='black', activebackground = 'gray93',
                            activeforeground = 'black', command = self.saida,width = 4)
        self.label1 = Label(self.frame, text='Converter para:',fg='black',font=("Helvetica", 12))
        self.labelEntrada.grid(row=0, column=0, sticky="w",pady=15,padx=20)
        self.botaoEntrada.grid(row=0,column=0,padx=180)
        self.botaoSaida.grid(row=4,column=0,padx=180)
        self.label1.grid(row=1, column=0, sticky="w",pady=15,padx=20)
        self.labelSaida.grid(row=4, column=0, sticky="w",pady=15,padx=20)
        self.rb1 = Radiobutton(self.frame, text=self.formatos[0], variable =  self.nome_formato, value = self.formatos[0],
                          command = self.select1)
        self.rb2 = Radiobutton(self.frame, text=self.formatos[1], variable =  self.nome_formato, value = self.formatos[1],
                          command = self.select2)
        self.rb1.grid(row=2, column=0, sticky="w",padx=20)
        self.rb2.grid(row=3, column=0, sticky="w",padx=20)
        self.botaoOK = Button(self.frame, text=' Converter ', bg = 'gray90',fg='black',width=8,font=("Helvetica", 11),
                              activebackground = 'gray93', activeforeground = 'black', command = self.formatar)
        self.botaoX = Button(self.frame, text='Cancelar', bg = 'gray90',fg='black',width=8,font=("Helvetica", 11),
                             activebackground = 'gray93',activeforeground = 'black', command = self.cancelar)
        self.botaoOK.grid(row=5, column=0,sticky='w',padx=20,pady=20)
        self.botaoX.grid(row=5, column=0)
        self.warning = Label(self.frame, text='',fg = 'red',font=("Helvetica", 11))
        self.warning.grid(row = 6, column = 0, sticky='w',padx=20)
        self.resizable(0,0)
        self.select = False
        self.Arquivos = ''
        self.liststreams = []
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        self.mainloop()

    def fechar(self):

        if messagebox.askyesno("Geosis - Siscon", "Sair do programa?"):

            self.destroy()

        else:

            pass
        
    def entrada(self):
         
        self.Arquivos = filedialog.askopenfilenames(title='Abrir',filetypes=(('seg2','*.dat'),
                                                ('segy','*.sgy'),('mseed','*.mseed'),('Todos os arquivos','*.*')))

        try:
            
            for i in self.Arquivos:
                self.liststreams.append(read(i))

            entradaOK = Label(self.frame, text='OK',fg = 'blue',font=("Helvetica", 11))
            entradaOK.grid(row=0,column=0,sticky='e',padx=150)

        except:

            messagebox.showerror('Geosis - Siscon','Arquivo inválido')

    def saida(self):

        self.arquivoSaida = filedialog.asksaveasfilename(title='Salvar',filetypes=[('segy','*.sgy'),('mseed','*.mseed')])
                                                        
        if len(self.arquivoSaida)>0:
            
            saidaOK = Label(self.frame, text='OK',fg = 'blue',font=("Helvetica", 11))
            saidaOK.grid(row=4,column=0,sticky='e',padx=150)
            
        else:
            
            pass
                
    def formatar(self):

        if len(self.Arquivos) == 0:

            self.warning.configure(text='Nenhum arquivo selecionado')

        elif self.select == False:

            self.warning.configure(text='Marque uma opção')

        elif len(self.arquivoSaida) == 0:

            self.warning.configure(text='Escolha o diretório de saída')
        
        elif self.select == True and len(self.Arquivos) > 0 and len(self.arquivoSaida) > 0:
            
            if self.nome_formato.get() == 'SEGY':

                try:
                    
                    for i in self.liststreams:
                        
                        i.write(self.arquivoSaida+'.sgy',format=self.nome_formato.get())

                    messagebox.showinfo('Geosis - Siscon','Conversão concluida')
                    
                except:

                    messagebox.showerror('Geosis - Siscon','Formato inválido')

            elif self.nome_formato.get() == 'MSEED':

                try:
                     
                    for i in self.liststreams:
                        
                        i.write(self.arquivoSaida+'.mseed',format=self.nome_formato.get())
                        
                    messagebox.showinfo('Geosis - Siscon','Conversão concluida')

                except:

                    messagebox.showerror('Geosis - Siscon','Formato inválido')

            else:

                pass
            
            for i in self.liststreams:
                
                del self.liststreams[:]
                
            self.frame.destroy()
            self.destroy()

        else:

            pass
        
    def cancelar(self):

        for i in self.liststreams:
                
            del self.liststreams[:]

        self.frame.destroy()
        self.destroy()

    def select1(self):

        self.select = True
        self.nome_formato.set(self.formatos[0])
        
    def select2(self):

        self.select = True
        self.nome_formato.set(self.formatos[1])
                
run = Launcher()
run.mainloop()