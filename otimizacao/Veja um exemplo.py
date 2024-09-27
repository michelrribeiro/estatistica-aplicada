import streamlit as st

# st.title insere o título principal da página com formatação automática;
# st.image insere uma imagem definida, porém o caminho completo foi necessário para contornar erros de leitura;
# st.markdown insere um texto com formatação markdown, incluindo cores, emoticons e etc.

st.set_page_config(page_title='Exemplo', layout='wide')

st.markdown('### Exemplo de modelagem de um problema de minimização')

st.write('Suponha uma empresa de logística que produz e exporta suco. Essa empresa gostaria de otimizar seus custos (ou seja, minimizar) a partir da existência de 3 fábricas produtoras e cinco mercados/destinos, sendo que o objetivo é escoar toda a produção com o menor custo possível.')

# Para a imagem foi utilizado o caminho absoluto para evitar erros na leitura da imagem:
img = r'/home/michelrribeiro/Downloads/posGraduacao2024/scripts-python/estatistica-aplicada/otimizacao/otimizacao-quadro-1.jpeg'
st.image(img)

st.write('Sendo assim, pode-se considerar cada variável $xij$ como sendo a combinação da região $i$ com o mercado $j$. As variáveis de decisão então serão:') 
st.markdown('''x11 = custo de escoamento da produção do RS no Mercosul;  
x21 = preço do escoamento da produção de MG no Mercosul;  
e assim por diante.''')
st.write('Dessa maneira pode-se obter a seguinte função objetivo:')
st.write('> FO = 53x11 + 76x12 + 142x13 + 278x14 + 254x15 + 61x21 + 84x22 + 151x23 + 287x24 + 269x25 + 111x31 + 132x32 + 116x33 + 304x34 + 284x35')

st.write('Para as restrições tem-se que toda a produção deve ser escoada e toda a demanda deve ser atendida, além da restrição de não negatividade para cada $xij$ onde o limite inferior é zero, ou seja:')
st.markdown('''x11 + x12 + x13 + x14 + x15 = 769 (produção no RS)  
x21 + x22 + x23 + x24 + x25 = 960 (produção em MG)  
x31 + x32 + x33 + x34 + x35 = 190 (produção em SP)  
x11 + x21 + x31 = 19 (demanda no Mercosul)  
x12 + x22 + x32 = 6 (demanda no México)  ''')
st.write('''x13 + x23 + x33 = 1650 (demanda nos EUA)  
x14 + x24 + x34 = 162 (demanda na China)  
x15 + x25 + x35 = 60 (demanda na UE)  ''')

st.markdown('$xij$ >= 0')

st.write('A partir da equação de função objetivo e das restrições compostas por equações e inequações o problema pode ser modelado e inserido na aplicação de otimização.')