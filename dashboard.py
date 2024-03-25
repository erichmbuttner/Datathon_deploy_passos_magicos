import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

df_Dist_mun = pd.read_csv('Distorcao_idade_serie_municipio_qedu.csv', encoding='cp1252',sep=';')
df_Ideb_mun = pd.read_csv('ideb_municipio.csv', encoding='cp1252',sep=';')
df_seab_mun = pd.read_csv('saeb_aprendizado_municipio.csv', encoding='cp1252',sep=';')
df_passos = pd.read_csv('PEDE_PASSOS_DATASET_FIAP_limpa.csv', encoding='UTF-8',sep=';')
df_passos_pivot = pd.read_csv('PEDE_PASSOS_DATASET_FIAP_PIVOT.csv',encoding='ISO-8859-1',sep=';')

tab1, tab2 = st.tabs(["Dashboard Passos Magicos", "Dashboard Educação"])

with tab1:
    st.title('Dashboard da Passos Mágicos')
    
    tab6, tab7 = st.tabs([":clipboard: Data Frame", ":chart_with_upwards_trend: Gráficos"])
    
    with tab6:
        
        st.write('Dataframe com os dados para pesquisa')
        # Filtros para o dashboard
        col7, col8 = st.columns(2)
        
        with col7:
            nomes = df_passos['NOME'].unique()
            
            nome_selecionado     = st.multiselect('Nome', nomes)
            if len(nome_selecionado) > 0:
                df_passos_filtrado = df_passos[df_passos['NOME'].isin(nome_selecionado)]

        with col8:
            instituicao = df_passos['INSTITUICAO_ENSINO_ALUNO_2020'].unique()
            inst_selecionado     = st.multiselect('Instituição', instituicao)
            
            if len(inst_selecionado) > 0:
                if len(nome_selecionado) > 0:
                    df_passos_filtrado = df_passos[(df_passos['INSTITUICAO_ENSINO_ALUNO_2020'].isin(inst_selecionado)) & (df_passos['NOME'].isin(nome_selecionado))]
                else:
                    df_passos_filtrado = df_passos[df_passos['INSTITUICAO_ENSINO_ALUNO_2020'].isin(inst_selecionado)]
                        
        if not nome_selecionado and not inst_selecionado:
            st.dataframe(df_passos, use_container_width=True)
        else:
            st.dataframe(df_passos_filtrado, use_container_width=True)
    
    with tab7:
        df_passos_pivot = df_passos_pivot[~df_passos_pivot['PEDRA'].isin(['#NULO!', 'D9891/2A'])]
        df_passos_pivot['DESTAQUE_IEG'] = df_passos_pivot['DESTAQUE_IEG'].replace({'Ponto a melhorar em 2021:': 'Melhorar:', 'Seu destaque em 2020:': 'Destaque:'}, regex=True)
        df_passos_pivot['DESTAQUE_IDA'] = df_passos_pivot['DESTAQUE_IDA'].replace({'Ponto a melhorar em 2021:': 'Melhorar:', 'Seu destaque em 2020:': 'Destaque:'}, regex=True)
        df_passos_pivot['DESTAQUE_IPV'] = df_passos_pivot['DESTAQUE_IPV'].replace({'Ponto a melhorar em 2021:': 'Melhorar:', 'Seu destaque em 2020:': 'Destaque:'}, regex=True)
        # Gráficos para o dashboard

        col9, col10 = st.columns(2)
        
        with col9:
            nomes_col9 = df_passos_pivot['NOME'].unique()
            nomes_selec = st.multiselect('Nome', nomes_col9)

        with col10:
            anos_col9 = df_passos_pivot['Ano'].unique()
            anos_selec = st.multiselect('Ano', anos_col9)
        
        if len(nomes_selec) > 0 :
            # Filtrar o DataFrame pelos nomes e anos selecionados
            df_filtrado_nome = df_passos_pivot[df_passos_pivot['NOME'].isin(nomes_selec)]
        else:
            df_filtrado_nome = df_passos_pivot
            
        if len(anos_selec) > 0: 
            if len(nomes_selec) > 0:
                df_filtrado_ano = df_passos_pivot[(df_passos_pivot['Ano'].isin(anos_selec)) & (df_passos_pivot['NOME'].isin(nomes_selec))]
            else:
                df_filtrado_ano = df_passos_pivot[df_passos_pivot['Ano'].isin(anos_selec)]
        else:
            df_filtrado_ano = df_passos_pivot
        
        # Agrupar por 'Ano' e 'PEDRA' e contar o número de alunos
        df_grouped_nome = df_filtrado_nome.groupby(['Ano', 'PEDRA']).size().reset_index(name='Quantidade')
        df_grouped_ano = df_filtrado_ano.groupby('PEDRA').size()
        
        # Criar subplots
        fig13, axs = plt.subplots(3, 1, figsize=(10, 15))
        
        # Gráfico de barras empilhadas
        df_grouped_nome.pivot(index='Ano', columns='PEDRA', values='Quantidade').plot(kind='bar', stacked=True, ax=axs[0])
        axs[0].set_title('Evolução dos alunos pelas classificações por ano acumulado')
        axs[0].set_xlabel('Ano')
        axs[0].set_ylabel('Quantidade de Alunos')
        
        # Gráfico de linhas
        for pedra in df_grouped_nome['PEDRA'].unique():
            df_pedra = df_grouped_nome[df_grouped_nome['PEDRA'] == pedra]
            axs[1].plot(df_pedra['Ano'], df_pedra['Quantidade'], label=pedra)
        axs[1].xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        axs[1].set_title('Evolução dos alunos selecionados pelas classificações atingidas por ano')
        axs[1].set_xlabel('Ano')
        axs[1].set_ylabel('Quantidade de Alunos')
        
        # Gráfico de pizza
        axs[2].pie(df_grouped_ano, labels = df_grouped_ano.index, autopct='%1.1f%%')
        axs[2].set_title('Percentual de classificação no ano selecionado')
        
        plt.tight_layout()
        plt.show()
        st.pyplot(fig13)
with tab2:
    # Criando o dashboard com Streamlit
    st.title('Dashboard de Sucesso Escolar')
    st.write('Fonte de dados : https://www.qedu.org.br/')
    
    st.write('O objetivo deste dashboard é apresentar os dados de distorção idade-série, IDEB e SEAB para o município de Embu-Guaçu. Com estes dados é possivel efetuar uma melhor avaliação dos alunos e melhoria dos indicadores do municipio de Embu-Guaçu.')

    tab3, tab4, tab5 = st.tabs([":chart_with_upwards_trend: Distorção Idade Série", ":bar_chart: IDEB", ":bar_chart: SEAB"])
    
    with tab3:
        st.write('Conheça a proporção de alunos com atraso escolar de 2 anos ou mais, para todo o Ensino Básico.')
        # Mapeando os valores numéricos para os nomes correspondentes
        mapa_localizacao = {0: 'Total', 1: 'Urbana', 2: 'Rural'}
        df_Dist_mun['localizacao_id'] = df_Dist_mun['localizacao_id'].map(mapa_localizacao)

        mapa_dependencia = {0: 'Total', 1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada', 5: 'Pública'}
        df_Dist_mun['dependencia_id'] = df_Dist_mun['dependencia_id'].map(mapa_dependencia)


        anos_unicos = df_Dist_mun['ano'].unique()
        depend_unicos = df_Dist_mun['dependencia_id'].unique()
        local_unicos = df_Dist_mun['localizacao_id'].unique()

        # Filtro para seleção
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            ano_selecionado     = st.selectbox('Ano', anos_unicos)

        with col2:
            depend_selecionado  = st.selectbox('Dependencia', depend_unicos)

        with col3:
            local_selecionado = st.selectbox('Local', local_unicos)

        with col4:
            serie_selecionado = st.selectbox('Série', ['Anos Iniciais', 'Anos Finais', 'Ensino Médio'])

        df_Dist_filtro = df_Dist_mun[df_Dist_mun['ano'] == ano_selecionado]
        df_Dist_filtro = df_Dist_mun[df_Dist_mun['dependencia_id'] == depend_selecionado]
        df_Dist_filtro = df_Dist_mun[df_Dist_mun['localizacao_id'] == local_selecionado]

        # Gráfico de Linhas

        fig, ax = plt.subplots(figsize=(20, 10))  # Ajuste o tamanho aqui conforme necessário

        st.write('Evolução da distorção idade-série')

        # Plotando o gráfico de linhas Anos iniciais
        if (serie_selecionado == 'Anos Iniciais'):
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['ef_1ano'], marker='o')
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['ef_2ano'], marker='o')
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['ef_3ano'], marker='o')
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['ef_4ano'], marker='o')
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['ef_5ano'], marker='o')
            plt.title('Evolução da distorção idade-série - Anos Iniciais - Embu-Guaçu')
            plt.xlabel('Ano')
            plt.ylabel('Percentual de distorção idade-série - Anos Iniciais')
            plt.grid(True)
            plt.legend(['1º ano', '2º ano', '3º ano', '4º ano', '5º ano'])
            plt.show()
            
        if (serie_selecionado == 'Anos Finais'):
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['ef_6ano'], marker='o')
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['ef_7ano'], marker='o')
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['ef_8ano'], marker='o')
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['ef_9ano'], marker='o')
            plt.title('Evolução da distorção idade-série - Anos Finais - Embu-Guaçu')
            plt.xlabel('Ano')
            plt.ylabel('Percentual de distorção idade-série - Anos Finais')
            plt.grid(True)
            plt.legend(['6º ano', '7º ano', '8º ano', '9º ano'])
            plt.show()

        if (serie_selecionado == 'Ensino Médio'):
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['em_1ano'], marker='o')
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['em_2ano'], marker='o')
            ax.plot(df_Dist_filtro['ano'], df_Dist_filtro['em_3ano'], marker='o')
            plt.title('Evolução da distorção idade-série - Ensino Médio - Embu-Guaçu')
            plt.xlabel('Ano')
            plt.ylabel('Percentual de distorção idade-série - Ensino Médio')
            plt.grid(True)
            plt.legend(['1º ano', '2º ano', '3º ano'])
            plt.show()

        # Exibindo o gráfico no Streamlit
        st.pyplot(fig)

    with tab4:
        # Tabela de Dados IDEB

        # Mapeando os valores numéricos para os nomes correspondentes
        mapa_dependencia = {0: 'Total', 1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada', 5: 'Pública'}
        df_Ideb_mun['dependencia_id'] = df_Ideb_mun['dependencia_id'].map(mapa_dependencia)

        mapa_serie = {'AF': 'Anos Finais', 'AI': 'Anos Iniciais', 'EM': 'Ensino Medio'}
        df_Ideb_mun['ciclo_id'] = df_Ideb_mun['ciclo_id'].map(mapa_serie)

        anos_unicos = df_Ideb_mun['ano'].unique()
        depend_unicos = df_Ideb_mun['dependencia_id'].unique()
        serie_unicos = df_Ideb_mun['ciclo_id'].unique()

        # Filtro para seleção
        col1, col2, col3 = st.columns(3)
        with col1:
            ano_selecionado     = st.selectbox('Ano', anos_unicos)

        with col2:
            depend_selecionado  = st.selectbox('Dependencia', depend_unicos)

        with col3:
            serie_selecionado = st.selectbox('Série', serie_unicos)

        df_IDEB_filtro = df_Ideb_mun[df_Ideb_mun['ano'] == ano_selecionado]
        df_IDEB_filtro = df_Ideb_mun[df_Ideb_mun['dependencia_id'] == depend_selecionado]
        df_IDEB_filtro = df_Ideb_mun[df_Ideb_mun['ciclo_id'] == serie_selecionado]

        st.write('IDEB')
        st.write('O Ideb é calculado com base no aprendizado dos alunos em português e matemática (Saeb) e no fluxo escolar (taxa de aprovação).')

        # Gráfico de Barras
        anos = df_Ideb_mun['ano'].unique() 
        df_IDEB_municipio_filtro = df_Ideb_mun[df_Ideb_mun['dependencia_id'] == depend_selecionado]
        dicionario = df_IDEB_municipio_filtro.groupby(['ciclo_id'])['ideb'].apply(list).to_dict()

        x = np.arange(len(anos))  # the label locations
        width = 0.25  # the width of the bars
        multiplier = 0

        fig2, ax2 = plt.subplots(layout='constrained')

        for serie, ideb in dicionario.items():
            offset = width * multiplier
            rects = ax2.bar(x + offset , ideb, width, label=serie)
            ax2.bar_label(rects, padding=3)
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax2.set_ylabel('IDEB')
        ax2.set_title('IDEB x anos')
        ax2.set_xticks(x + width, anos)
        ax2.legend(loc='upper left', ncols=3)
        ax2.set_ylim(0, 10)

        plt.show()
        st.pyplot(fig2)
        
    with tab5:
        
        # Tabela de Dados SEAB

        # Mapeando os valores numéricos para os nomes correspondentes
        mapa_dependencia = {0: 'Total', 1: 'Federal', 2: 'Estadual', 3: 'Municipal', 4: 'Privada', 5: 'Pública'}
        df_seab_mun['dependencia_id'] = df_seab_mun['dependencia_id'].map(mapa_dependencia)

        mapa_serie = {'AF': 'Anos Finais', 'AI': 'Anos Iniciais', 'EM': 'Ensino Medio'}
        df_seab_mun['ciclo_id'] = df_seab_mun['ciclo_id'].map(mapa_serie)

        anos_seab_unicos = df_seab_mun['ano'].unique()
        depend_seab_unicos = df_seab_mun['dependencia_id'].unique()
        serie_seab_unicos = df_seab_mun['ciclo_id'].unique()

        # Filtro para seleção
        col1, col2, col3 = st.columns(3)
        with col1:
            ano_seab_selecionado     = st.selectbox('Ano Seab', anos_seab_unicos)

        with col2:
            depend_seab_selecionado  = st.selectbox('Dependencia Seab', depend_seab_unicos)

        with col3:
            serie_seab_selecionado = st.selectbox('Série Seab', serie_seab_unicos)

        df_SEAB_filtro = df_seab_mun[df_seab_mun['ano'] == ano_seab_selecionado]
        df_SEAB_filtro = df_seab_mun[df_seab_mun['dependencia_id'] == depend_seab_selecionado]
        df_SEAB_filtro = df_seab_mun[df_seab_mun['ciclo_id'] == serie_seab_selecionado]

        st.write('Indicador de Aprendizado SEAB')
        st.write('O indicador de aprendizado varia de 0 até 10 e quanto maior, melhor. Porém, o 10 é praticamente inatingível, significaria que todos alunos obtiveram rendimento esperado')

        df_seab_mun['lp_adequado'] = df_seab_mun['lp_adequado'] * 100
        df_seab_mun['lp_insuficiente'] = df_seab_mun['lp_insuficiente'] * 100
        df_seab_mun['lp_basico'] = df_seab_mun['lp_basico'] * 100
        df_seab_mun['lp_proficiente'] = df_seab_mun['lp_proficiente'] * 100
        df_seab_mun['lp_avancado'] = df_seab_mun['lp_avancado'] * 100
        df_seab_mun['mt_adequado'] = df_seab_mun['mt_adequado'] * 100
        df_seab_mun['mt_insuficiente'] = df_seab_mun['mt_insuficiente'] * 100
        df_seab_mun['mt_basico'] = df_seab_mun['mt_basico'] * 100
        df_seab_mun['mt_proficiente'] = df_seab_mun['mt_proficiente'] * 100
        df_seab_mun['mt_avancado'] = df_seab_mun['mt_avancado'] * 100
        
        
        # Gráfico de Barras
        anos = df_seab_mun['ano'].unique() 
        df_seab_municipio_filtro = df_seab_mun[df_seab_mun['dependencia_id'] == depend_seab_selecionado]
        dic_lp_adequado = df_seab_municipio_filtro.groupby(['ciclo_id'])['lp_adequado'].apply(list).to_dict()
        dic_lp_insuficiente = df_seab_municipio_filtro.groupby(['ciclo_id'])['lp_insuficiente'].apply(list).to_dict()
        dic_lp_basico = df_seab_municipio_filtro.groupby(['ciclo_id'])['lp_basico'].apply(list).to_dict()
        dic_lp_proficiente = df_seab_municipio_filtro.groupby(['ciclo_id'])['lp_proficiente'].apply(list).to_dict()
        dic_lp_avancado = df_seab_municipio_filtro.groupby(['ciclo_id'])['lp_avancado'].apply(list).to_dict()
        dic_mt_adequado = df_seab_municipio_filtro.groupby(['ciclo_id'])['mt_adequado'].apply(list).to_dict()
        dic_mt_insuficiente = df_seab_municipio_filtro.groupby(['ciclo_id'])['mt_insuficiente'].apply(list).to_dict()
        dic_mt_basico = df_seab_municipio_filtro.groupby(['ciclo_id'])['mt_basico'].apply(list).to_dict()
        dic_mt_proficiente = df_seab_municipio_filtro.groupby(['ciclo_id'])['mt_proficiente'].apply(list).to_dict()
        dic_mt_avancado = df_seab_municipio_filtro.groupby(['ciclo_id'])['mt_avancado'].apply(list).to_dict()


        col_rel1, col_rel2 = st.columns(2)
        with col_rel1:
            #Percentual de aprendizado Matematica Adequado
            
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig8, ax8 = plt.subplots(layout='constrained')

            for serie, mt_adequado in dic_mt_adequado.items():
                offset = width * multiplier
                rects = ax8.bar(x + offset , mt_adequado, width, label=serie)
                ax8.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax8.set_ylabel('Percentual')
            ax8.set_title('Percentual de aprendizado Matematica Adequado')
            ax8.set_xticks(x + width, anos)
            ax8.legend(loc='upper left', ncols=3)
            ax8.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig8)

            
            #Percentual de aprendizado Matematica Insuficiente
                    
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig9, ax9 = plt.subplots(layout='constrained')

            for serie, mt_insuficiente in dic_mt_insuficiente.items():
                offset = width * multiplier
                rects = ax9.bar(x + offset , mt_insuficiente, width, label=serie)
                ax9.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax9.set_ylabel('Percentual')
            ax9.set_title('Percentual de aprendizado Matematica Insuficiente')
            ax9.set_xticks(x + width, anos)
            ax9.legend(loc='upper left', ncols=3)
            ax9.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig9)
            
            #Percentual de aprendizado Matematica Basico
                    
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig10, ax10 = plt.subplots(layout='constrained')

            for serie, mt_basico in dic_mt_basico.items():
                offset = width * multiplier
                rects = ax10.bar(x + offset , mt_basico, width, label=serie)
                ax10.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax10.set_ylabel('Percentual')
            ax10.set_title('Percentual de aprendizado Matematica Basico')
            ax10.set_xticks(x + width, anos)
            ax10.legend(loc='upper left', ncols=3)
            ax10.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig10)
            
            #Percentual de aprendizado Matematica Proficiente
                    
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig11, ax11 = plt.subplots(layout='constrained')

            for serie, mt_proficiente in dic_mt_proficiente.items():
                offset = width * multiplier
                rects = ax11.bar(x + offset , mt_proficiente, width, label=serie)
                ax11.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax11.set_ylabel('Percentual')
            ax11.set_title('Percentual de aprendizado Matematica Proficiente')
            ax11.set_xticks(x + width, anos)
            ax11.legend(loc='upper left', ncols=3)
            ax11.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig11)        

            #Percentual de aprendizado Matematica Avançado
                    
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig12, ax12 = plt.subplots(layout='constrained')

            for serie, mt_avancado in dic_mt_avancado.items():
                offset = width * multiplier
                rects = ax12.bar(x + offset , mt_avancado, width, label=serie)
                ax12.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax12.set_ylabel('Percentual')
            ax12.set_title('Percentual de aprendizado Matematica Avançado')
            ax12.set_xticks(x + width, anos)
            ax12.legend(loc='upper left', ncols=3)
            ax12.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig12)

        with col_rel2:
            #Percentual de aprendizado Lingua Portuguesa Adequado
            
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig3, ax3 = plt.subplots(layout='constrained')

            for serie, lp_adequado in dic_lp_adequado.items():
                offset = width * multiplier
                rects = ax3.bar(x + offset , lp_adequado, width, label=serie)
                ax3.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax3.set_ylabel('Percentual')
            ax3.set_title('Percentual de aprendizado Lingua Portuguesa Adequado')
            ax3.set_xticks(x + width, anos)
            ax3.legend(loc='upper left', ncols=3)
            ax3.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig3)

            
            #Percentual de aprendizado Lingua Portuguesa Insuficiente
                    
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig4, ax4 = plt.subplots(layout='constrained')

            for serie, lp_insuficiente in dic_lp_insuficiente.items():
                offset = width * multiplier
                rects = ax4.bar(x + offset , lp_insuficiente, width, label=serie)
                ax4.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax4.set_ylabel('Percentual')
            ax4.set_title('Percentual de aprendizado Lingua Portuguesa Insuficiente')
            ax4.set_xticks(x + width, anos)
            ax4.legend(loc='upper left', ncols=3)
            ax4.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig4)
            
            #Percentual de aprendizado Lingua Portuguesa Basico
                    
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig5, ax5 = plt.subplots(layout='constrained')

            for serie, lp_basico in dic_lp_basico.items():
                offset = width * multiplier
                rects = ax5.bar(x + offset , lp_basico, width, label=serie)
                ax5.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax5.set_ylabel('Percentual')
            ax5.set_title('Percentual de aprendizado Lingua Portuguesa Basico')
            ax5.set_xticks(x + width, anos)
            ax5.legend(loc='upper left', ncols=3)
            ax5.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig5)
            
            #Percentual de aprendizado Lingua Portuguesa Proficiente
                    
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig6, ax6 = plt.subplots(layout='constrained')

            for serie, lp_proficiente in dic_lp_proficiente.items():
                offset = width * multiplier
                rects = ax6.bar(x + offset , lp_proficiente, width, label=serie)
                ax6.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax6.set_ylabel('Percentual')
            ax6.set_title('Percentual de aprendizado Lingua Portuguesa Proficiente')
            ax6.set_xticks(x + width, anos)
            ax6.legend(loc='upper left', ncols=3)
            ax6.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig6)        

            #Percentual de aprendizado Lingua Portuguesa Avançado
                    
            x = np.arange(len(anos))  # the label locations
            width = 0.25  # the width of the bars
            multiplier = 0

            fig7, ax7 = plt.subplots(layout='constrained')

            for serie, lp_avancado in dic_lp_avancado.items():
                offset = width * multiplier
                rects = ax7.bar(x + offset , lp_avancado, width, label=serie)
                ax7.bar_label(rects, padding=3)
                multiplier += 1

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax7.set_ylabel('Percentual')
            ax7.set_title('Percentual de aprendizado Lingua Portuguesa Avançado')
            ax7.set_xticks(x + width, anos)
            ax7.legend(loc='upper left', ncols=3)
            ax7.set_ylim(0, 100)

            plt.show()
            st.pyplot(fig7)        
