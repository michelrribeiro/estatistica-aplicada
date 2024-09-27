import re
import streamlit as st
from pulp import LpMaximize, LpMinimize, LpProblem, lpSum, LpVariable

# Configuração com nome da página a ser exibida no navegador:
st.set_page_config(page_title='Solver', layout='wide')

# Configuração para todos os botões e todas as caixas de texto da página:
st.markdown('''<style>
                  button {height: 1.55em;}
            </style>''', unsafe_allow_html=True)

# Título da página:
st.markdown('### Encontre o ponto de máximo ou de mínimo para o problema modelado')

# Opções a serem definidas pelo usuário nas listas suspensas na barra lateral:
goals = ['Maximizar o resultado', 'Minimizar o resultado']
#methods = ['Simplex com SciPy', 'GLPK com PuLP']

goal = st.sidebar.selectbox('Escolha o objetivo da otimização:', goals)
#method = st.sidebar.selectbox('Escolha o método a ser utilizado:', methods)

# Cria as listas de equações de restrição, inequações de restrição e o modelo:
if 'obj_func' not in st.session_state:
    st.session_state.obj_func = None

if 'eqs' not in st.session_state:
    st.session_state.eqs = []

if 'ineqs' not in st.session_state:
    st.session_state.ineqs = []

# Caixa de texto para inserção da função objetivo no padrão esperado:
obj_func = st.text_input('Digite a função objetivo a ser otimizada. Utilize xij no padrão 1x11 + 1x12 + ... + 1xnn.')

# Botão para salvar a FO:
if st.button('Definir F.O.') and re.sub('[0-9|x\ \-\+\=]', '', obj_func) == '':
    if obj_func:
        st.session_state.obj_func = obj_func
        st.success('Função objetivo criada com sucesso.')
    else:
        st.error('Por favor, defina a função objetivo do problema com variáves xij.')

# Criando as duas colunas lado a lado:
col1, col2 = st.columns((1,1))

# Caixa de texto para inserção de equações de restrição:
eq = col1.text_input('Digite a equação de restrição e depois clique em Inserir. Utilize xij no padrão 1x11 + 1x12 = 1.')

# Botão para inserir a equação de restrição:
if col1.button('Inserir equação'):
    if eq and re.sub('[0-9A-Za-z|\ \-\+\=]', '', eq) == '':
        if eq in st.session_state.eqs:
            st.sucess('Equação já inserida anteriormente.')
        else:
            st.session_state.eqs.append(eq)
            st.success('Equação de restrição inserida com sucesso.')
    else:
        st.error('Erro ao inserir equação.')

# Caixa de texto para inserção de equações de restrição:
ineq = col2.text_input('Digite a inequação de restrição e depois clique em Inserir. Utilize xij no padrão 1x11 + 1x12 >= 1 ou 1x11 + 1x12 <= 1.')

# Botão para inserir a inequação de restrição:
if col2.button('Inserir inequação'):
    if ineq and re.sub('[0-9A-Za-z\ \+\-\=\>\<]', '', ineq) == '':
        if ineq in st.session_state.ineqs:
            st.sucess('Inequação já inserida anteriormente.')
        else:
            st.session_state.ineqs.append(ineq)
            st.success('Inequação de restrição inserida com sucesso.')
    else:
        st.error('Erro ao inserir inequação.')

col1.markdown('###### Confirme as equações antes de confirmar o processamento:')
col2.markdown('###### Confirme as inequações antes de confirmar o processamento:')

if len(st.session_state.eqs) > 0:
    col1.markdown('Equações de igualdade aplicáveis ao problema:')
    for eq_constraint in st.session_state.eqs:
        col1.write(eq_constraint)
else:
    pass

if len(st.session_state.ineqs) > 0:
    col2.markdown('Equações de desigualdade aplicáveis ao problema:')
    for ineq_constraint in st.session_state.ineqs:
        col2.write(ineq_constraint)
else:
    pass

# Botão para limpar a lista
if st.button('Limpar lista'):
    st.session_state.eqs.clear()
    st.session_state.ineqs.clear()
    st.success('Quadro de variáveis limpo.')

# Botão para resolver a partir das escolhas na barra lateral:
if st.button('Solucionar o problema'):
    if not obj_func:
        st.error('Por favor, defina a função objetivo.')    
    else:
        # Criando o modelo:
        model = LpProblem(name='Otimização', sense=(LpMaximize if goal == 'Maximizar o resultado' else LpMinimize))
        # Padronizando a função objetivo e extraindo as variáveis de decisão:
        obj_func = obj_func.replace('x', '*x')
        fun = obj_func.replace(' ', '').replace('-', '+-').split('+')
        fun = [fun[n] for n in range(len(fun)) if fun[n] != '']
        dec_vars = [var[var.find('x'):] for var in fun]
        # Criando as variáveis de decisão:
        for var_name in dec_vars:
            tempName = var_name
            exec(f"{var_name} = LpVariable(name=tempName, lowBound=0)")
        # Adicionando a função objetivo:
        exec(f'model += ({obj_func})')
        # Adicionando igualdades:
        eq_constraint = [cons.replace('x', '*x').replace('=', '==').replace('===', '==') if cons[0] != 'x' 
                         else cons.replace('=', '==').replace('===', '==') for cons in st.session_state.eqs]
        for cons in eq_constraint:
            exec(f'model += ({cons})')
        # Adicionando desigualdades:
        ineq_constraint = [cons.replace('x', '*x') if cons[0] != 'x' 
                           else cons for cons in st.session_state.ineqs]
        for cons in ineq_constraint:
            exec(f'model += ({cons})')
        # Resolvendo o problema:
        solucao = model.solve()
        # Retornando os resultados finais:
        st.markdown('###### Resultado Final')
        valor_otimo = model.objective.value()
        finalSolver = ' + '.join([str(int(n.value()))+n.name for n in model.variables() if n.value() > 0])
        st.write(f'Valor ótimo encontrado: {valor_otimo}')
        st.write(f'Equação de otimização: ',finalSolver)