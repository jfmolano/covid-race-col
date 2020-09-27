#!/usr/bin/env python
# coding: utf-8

# In[1]:


import chart_studio.plotly as py
import plotly.graph_objects as go


# In[2]:


import plotly.express as px


# In[3]:


from plotly.subplots import make_subplots


# In[4]:


import pandas as pd


# In[5]:


import numpy as np


# In[6]:


import datetime


# In[7]:


import colorlover as cl


# In[8]:


from matplotlib import pyplot as plt


# In[9]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[10]:


df_censo = pd.read_excel("./CNPV-2018-VIHOPE-v2.xls")


# In[11]:


df_covid = pd.read_csv("https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD")


# In[12]:


df_covid["Departamento o Distrito "].unique()


# In[13]:


df_covid["Departamento o Distrito "] = df_covid["Departamento o Distrito "].apply(lambda x:"San Andrés, Providencia y S. Catalina" if x=="Archipiélago de San Andrés Providencia y Santa Catalina" else x)


# In[14]:


def parse(x):
    if x==x:
        try:
            return datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f')
        except:
            return pd.NaT
    else:
        return pd.NaT


# In[15]:


df_covid["Código DIVIPOLA"].isna().sum()


# In[16]:


date_cols = ["Fecha de notificación","FIS","Fecha de muerte","Fecha diagnostico","Fecha recuperado","fecha reporte web"]


# In[17]:


for columns in date_cols:
    df_covid[columns] = df_covid[columns].apply(parse)


# In[18]:


df_covid.columns


# In[19]:


(df_covid["FIS"].isna()).sum()


# In[20]:


df_covid["Estado"].value_counts()


# In[21]:


(df_covid["Fecha diagnostico"] - df_covid["FIS"]).quantile(0.9)


# In[22]:


df_covid["date"] = df_covid.apply(lambda x:x["FIS"] if pd.isna(x["FIS"]) else x["Fecha diagnostico"], axis=1)


# ___

# In[23]:


l_charts = []


# In[24]:


df_plot = df_covid.groupby(["date"]).count()["Código DIVIPOLA"].to_frame().reset_index()


# In[25]:


df_plot["m_avg"] = df_plot["Código DIVIPOLA"].rolling(window=7).mean()


# In[26]:


load_data_zone = (df_covid["Fecha diagnostico"] - df_covid["FIS"]).quantile(0.9)


# In[27]:


fig = px.line(x=df_plot['date'], y=df_plot["m_avg"])
fig.update_traces(line_color='black')
fig.add_bar(x=df_plot['date'], y=df_plot["Código DIVIPOLA"], marker_color="gray")
fig.update_layout(title_text="Casos diarios y promedio móvil de 7 días",showlegend=False)
fig.add_trace(
    go.Scatter(x=[df_plot["date"].max() - load_data_zone,df_plot["date"].max(),df_plot["date"].max(),df_plot["date"].max() - load_data_zone,df_plot["date"].max() - load_data_zone], y=[0,0,df_plot["Código DIVIPOLA"].max(),df_plot["Código DIVIPOLA"].max(),0], fill="toself", marker_color="gray", opacity=0.9, marker_size=1),
)
fig['layout']['yaxis']['title'] = "Casos diarios"
fig['layout']['xaxis']['title'] = "Fecha"
l_charts.append(fig)


# In[28]:


fig = make_subplots(rows=13, cols=3,
    subplot_titles=list(df_covid["Departamento o Distrito "].value_counts().index))

for n,depto in enumerate(list(df_covid["Departamento o Distrito "].value_counts().index)):
    
    df_filter_depto = df_covid.loc[df_covid["Departamento o Distrito "]==depto]
    
    load_data_zone = (df_filter_depto["Fecha diagnostico"] - df_filter_depto["FIS"]).quantile(0.9)
    
    df_filter_depto = df_filter_depto.groupby(["date"]).count()["Código DIVIPOLA"].to_frame().reset_index()
    
    df_filter_depto["m_avg"] = df_filter_depto["Código DIVIPOLA"].rolling(window=7).mean()

    fig.add_trace(
        go.Bar(x=df_filter_depto["date"], y=df_filter_depto["Código DIVIPOLA"],marker_color="gray"),
        row=(n//3+1), col=(n%3+1)
    )
    
    fig.add_trace(
        go.Scatter(x=df_filter_depto["date"], y=df_filter_depto["m_avg"],marker_color="black"),
        row=(n//3+1), col=(n%3+1)
    )
    
    fig.add_trace(
        go.Scatter(x=[df_filter_depto["date"].max() - load_data_zone,df_filter_depto["date"].max(),df_filter_depto["date"].max(),df_filter_depto["date"].max() - load_data_zone,df_filter_depto["date"].max() - load_data_zone], y=[0,0,df_filter_depto["Código DIVIPOLA"].max(),df_filter_depto["Código DIVIPOLA"].max(),0], fill="toself", marker_color="gray", opacity=0.9, marker_size=1),
        row=(n//3+1), col=(n%3+1)
    )

fig.update_layout(height=2500, width=900, title_text="Casos diarios por departamentos",showlegend=False)
l_charts.append(fig)


# In[29]:


for i in range(4):
    
    top = (i+1)*9+1 if i==3 else (i+1)*9

    fig = make_subplots(rows=(4 if i==3 else 3), cols=3,
        subplot_titles=list(df_covid["Departamento o Distrito "].value_counts().index)[i*9:top])

    for n,depto in enumerate(list(df_covid["Departamento o Distrito "].value_counts().index)[i*9:top]):

        df_filter_depto = df_covid.loc[df_covid["Departamento o Distrito "]==depto]

        load_data_zone = (df_filter_depto["Fecha diagnostico"] - df_filter_depto["FIS"]).quantile(0.9)

        df_filter_depto = df_filter_depto.groupby(["date"]).count()["Código DIVIPOLA"].to_frame().reset_index()

        df_filter_depto["m_avg"] = df_filter_depto["Código DIVIPOLA"].rolling(window=7).mean()

        fig.add_trace(
            go.Bar(x=df_filter_depto["date"], y=df_filter_depto["Código DIVIPOLA"],marker_color="gray"),
            row=(n//3+1), col=(n%3+1)
        )

        fig.add_trace(
            go.Scatter(x=df_filter_depto["date"], y=df_filter_depto["m_avg"],marker_color="black"),
            row=(n//3+1), col=(n%3+1)
        )

        fig.add_trace(
            go.Scatter(x=[df_filter_depto["date"].max() - load_data_zone,df_filter_depto["date"].max(),df_filter_depto["date"].max(),df_filter_depto["date"].max() - load_data_zone,df_filter_depto["date"].max() - load_data_zone], y=[0,0,df_filter_depto["Código DIVIPOLA"].max(),df_filter_depto["Código DIVIPOLA"].max(),0], fill="toself", marker_color="gray", opacity=0.9, marker_size=1),
            row=(n//3+1), col=(n%3+1)
        )

    fig.update_layout(height=1200 if i==3 else 900, width=900, title_text="Casos diarios por departamentos",showlegend=False)
    fig.write_image("casos_%s.png" % i)


# # Deaths

# In[30]:


df_covid.columns


# In[31]:


df_covid_death = df_covid.loc[~df_covid["Fecha de muerte"].isna()]
len(df_covid_death)


# In[32]:


df_plot = df_covid_death.groupby(["Fecha de muerte"]).count()["Código DIVIPOLA"].to_frame().reset_index()


# In[33]:


df_plot["m_avg"] = df_plot["Código DIVIPOLA"].rolling(window=7).mean()


# In[34]:


load_data_zone = (df_covid["Fecha diagnostico"] - df_covid["FIS"]).quantile(0.9)


# In[35]:


fig = px.line(x=df_plot['Fecha de muerte'], y=df_plot["m_avg"])
fig.update_traces(line_color='darkred')
fig.add_bar(x=df_plot['Fecha de muerte'], y=df_plot["Código DIVIPOLA"], marker_color="lightcoral")
fig.update_layout(title_text="Muertes diarias y promedio móvil de 7 días",showlegend=False)
fig.add_trace(
    go.Scatter(x=[df_plot["Fecha de muerte"].max() - load_data_zone,df_plot["Fecha de muerte"].max(),df_plot["Fecha de muerte"].max(),df_plot["Fecha de muerte"].max() - load_data_zone,df_plot["Fecha de muerte"].max() - load_data_zone], y=[0,0,df_plot["Código DIVIPOLA"].max(),df_plot["Código DIVIPOLA"].max(),0], fill="toself", marker_color="darkred", opacity=0.8, marker_size=1),
)
fig['layout']['yaxis']['title'] = "Muertes diarias"
fig['layout']['xaxis']['title'] = "Fecha"
l_charts.append(fig)


# In[36]:


fig = make_subplots(rows=13, cols=3,
    subplot_titles=list(df_covid_death["Departamento o Distrito "].value_counts().index))

for n,depto in enumerate(list(df_covid_death["Departamento o Distrito "].value_counts().index)):
    
    df_filter_depto = df_covid.loc[df_covid["Departamento o Distrito "]==depto]
    
    load_data_zone = (df_filter_depto["Fecha diagnostico"] - df_filter_depto["FIS"]).quantile(0.9)
    
    df_filter_depto = df_filter_depto.loc[~df_covid["Fecha de muerte"].isna()]
    
    df_filter_depto = df_filter_depto.groupby(["Fecha de muerte"]).count()["Código DIVIPOLA"].to_frame().reset_index()
    
    df_filter_depto["m_avg"] = df_filter_depto["Código DIVIPOLA"].rolling(window=7).mean()

    fig.add_trace(
        go.Bar(x=df_filter_depto["Fecha de muerte"], y=df_filter_depto["Código DIVIPOLA"],marker_color="darkred"),
        row=(n//3+1), col=(n%3+1)
    )
    
    fig.add_trace(
        go.Scatter(x=df_filter_depto["Fecha de muerte"], y=df_filter_depto["m_avg"],marker_color="darkred"),
        row=(n//3+1), col=(n%3+1)
    )
    
    fig.add_trace(
        go.Scatter(x=[df_filter_depto["Fecha de muerte"].max() - load_data_zone,df_filter_depto["Fecha de muerte"].max(),df_filter_depto["Fecha de muerte"].max(),df_filter_depto["Fecha de muerte"].max() - load_data_zone,df_filter_depto["Fecha de muerte"].max() - load_data_zone], y=[0,0,df_filter_depto["Código DIVIPOLA"].max(),df_filter_depto["Código DIVIPOLA"].max(),0], fill="toself", marker_color="darkred", opacity=0.9, marker_size=1),
        row=(n//3+1), col=(n%3+1)
    )

fig.update_layout(height=2500, width=900, title_text="Muertes diarias por departamentos",showlegend=False)
l_charts.append(fig)


# In[37]:


for i in range(4):
    
    top = (i+1)*9+1 if i==3 else (i+1)*9

    fig = make_subplots(rows=(4 if i==3 else 3), cols=3,
        subplot_titles=list(df_covid_death["Departamento o Distrito "].value_counts().index)[i*9:top])

    for n,depto in enumerate(list(df_covid_death["Departamento o Distrito "].value_counts().index)[i*9:top]):

        df_filter_depto = df_covid.loc[df_covid["Departamento o Distrito "]==depto]

        load_data_zone = (df_filter_depto["Fecha diagnostico"] - df_filter_depto["FIS"]).quantile(0.9)
        
        df_filter_depto = df_filter_depto.loc[~df_covid["Fecha de muerte"].isna()]

        df_filter_depto = df_filter_depto.groupby(["Fecha de muerte"]).count()["Código DIVIPOLA"].to_frame().reset_index()

        df_filter_depto["m_avg"] = df_filter_depto["Código DIVIPOLA"].rolling(window=7).mean()

        fig.add_trace(
            go.Bar(x=df_filter_depto["Fecha de muerte"], y=df_filter_depto["Código DIVIPOLA"],marker_color="darkred"),
            row=(n//3+1), col=(n%3+1)
        )

        fig.add_trace(
            go.Scatter(x=df_filter_depto["Fecha de muerte"], y=df_filter_depto["m_avg"],marker_color="darkred"),
            row=(n//3+1), col=(n%3+1)
        )

        fig.add_trace(
            go.Scatter(x=[df_filter_depto["Fecha de muerte"].max() - load_data_zone,df_filter_depto["Fecha de muerte"].max(),df_filter_depto["Fecha de muerte"].max(),df_filter_depto["Fecha de muerte"].max() - load_data_zone,df_filter_depto["Fecha de muerte"].max() - load_data_zone], y=[0,0,df_filter_depto["Código DIVIPOLA"].max(),df_filter_depto["Código DIVIPOLA"].max(),0], fill="toself", marker_color="darkred", opacity=0.9, marker_size=1),
            row=(n//3+1), col=(n%3+1)
        )

    fig.update_layout(height=1200 if i==3 else 900, width=900, title_text="Muertes diarias por departamentos",showlegend=False)
    fig.write_image("muertes_%s.png" % i)


# In[38]:


df_rolling_deaths = df_covid_death.groupby(["Fecha de muerte","Departamento o Distrito "])["Código DIVIPOLA"].count().unstack().fillna(0).rolling(window=7).mean()


# In[39]:


load_data_zone


# In[40]:


l_peak_dates = []
for depto in df_rolling_deaths.columns:
    #print(depto)
    max_date = list(df_rolling_deaths[depto].to_frame().loc[df_rolling_deaths[depto]==df_rolling_deaths[depto].max()].tail(1).index)[0]
    #print(max_date)
    l_peak_dates.append(
        {"start_date":max_date,"end_date":max_date+pd.Timedelta('2 days'),"depto":depto}
    )


# In[41]:


df_peak_dates = pd.DataFrame(l_peak_dates)


# In[42]:


l_labels = []
for n,d in enumerate(df_peak_dates.sort_values("start_date").to_dict(orient="records")):
    l_labels.append(
        dict(
            x=d["end_date"]+pd.Timedelta('5 days'),
            y=len(df_peak_dates)-(n+1),
            text=d["depto"],
            showarrow=False,
            font=dict(color='black',size=12)
        )
    )


# In[43]:


l_order = list(df_peak_dates.sort_values("start_date")["depto"])


# In[44]:


fig = px.timeline(df_peak_dates, x_start="start_date", x_end="end_date", y="depto",category_orders={"depto":l_order})
fig.update_layout(height=700, title_text="Fecha del máximo valor en promedio de muertes por departamento",showlegend=False)
fig['layout']['annotations'] = l_labels
fig['layout']['yaxis']['showticklabels'] = False
fig['layout']['yaxis']['visible'] = False
fig['layout']['xaxis']['dtick'] = "M1"

l_charts.append(fig)


# In[45]:


load_data_zone = (df_covid["Fecha diagnostico"] - df_covid["FIS"]).quantile(0.9)


# In[46]:


df_covid_cases_load = df_covid.loc[
    (df_covid["date"] < (df_covid["date"].max() - load_data_zone)) &
    (df_covid["date"] >= (df_covid["date"].max() - load_data_zone - pd.Timedelta('14 days')))
]


# In[47]:


df_covid_cases_load["week"] = df_covid_cases_load["date"].apply(lambda x:"current_week" if (x > (df_covid_cases_load["date"].max()-pd.Timedelta('7 days'))) else "previous_week")


# In[48]:


current_week_max = datetime.datetime.strftime(df_covid_cases_load.loc[df_covid_cases_load["week"]=="current_week"]["date"].max(), '%d-%m')
current_week_min = datetime.datetime.strftime(df_covid_cases_load.loc[df_covid_cases_load["week"]=="current_week"]["date"].min(), '%d-%m')
previous_week_max = datetime.datetime.strftime(df_covid_cases_load.loc[df_covid_cases_load["week"]=="previous_week"]["date"].max(), '%d-%m')
previous_week_min = datetime.datetime.strftime(df_covid_cases_load.loc[df_covid_cases_load["week"]=="previous_week"]["date"].min(), '%d-%m')


# In[49]:


df_covid_cases_per_pop = df_covid.loc[
    (df_covid["date"] < (df_covid["date"].max() - load_data_zone)) &
    (df_covid["date"] >= (df_covid["date"].max() - load_data_zone - pd.Timedelta('7 days')))
]


# In[50]:


df_covid_cases_per_pop = df_covid_cases_per_pop.groupby(["Código DIVIPOLA"]).count()["ID de caso"].reset_index()


# In[51]:


df_covid_cases_per_pop = pd.merge(df_censo,df_covid_cases_per_pop,on="Código DIVIPOLA", how="inner")


# In[52]:


df_covid_cases_per_pop["cases_per_pop"] = df_covid_cases_per_pop["ID de caso"]*1e5/df_covid_cases_per_pop["Población total"]


# In[53]:


df_select_table = df_covid_cases_per_pop.loc[(df_covid_cases_per_pop["Población total"]>50000)].sort_values("cases_per_pop", ascending=False)


# In[54]:


color_list = list(((df_select_table["cases_per_pop"].head(10).astype(int)/(df_select_table["cases_per_pop"].head(10).astype(int)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Purples'][x]))


# In[55]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Población', 'Casos semana %s a %s por 100K' % (current_week_min,current_week_max)]),
                 columnwidth = [70,60,90],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"].head(10) + ", " + df_select_table["NOMBRE DEPARTAMENTO"].head(10),
                     df_select_table["Población total"].head(10),
                     df_select_table["cases_per_pop"].head(10).astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)',color_list])
                ))
            ])
fig.update_layout(height=450, title_text="Municipios con más casos por 100.000 habitantes en la última semana antes de rezago",showlegend=False)
l_charts.append(fig)
#fig


# In[56]:


df_select_table = df_covid_cases_per_pop.sort_values("Población total", ascending=False).head(25).sort_values("cases_per_pop", ascending=False)


# In[57]:


color_list = list(((df_select_table["cases_per_pop"].head(10).astype(int)/(df_select_table["cases_per_pop"].head(10).astype(int)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Purples'][x]))


# In[58]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Población', 'Casos semana %s a %s por 100K' % (current_week_min,current_week_max)]),
                 columnwidth = [90,60,60],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"] + ", " + df_select_table["NOMBRE DEPARTAMENTO"],
                     df_select_table["Población total"].apply(lambda x:'{:,}'.format(x).replace(',', '.')),
                     df_select_table["cases_per_pop"].astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)',color_list])
                ))
            ])
fig.update_layout(height=750, title_text="Casos por 100K habitantes en la última semana antes de rezago",showlegend=False)
l_charts.append(fig)


# In[59]:


df_covid_death_per_pop = df_covid_death.loc[
    (df_covid_death["Fecha de muerte"] < (df_covid_death["Fecha de muerte"].max() - load_data_zone)) &
    (df_covid_death["Fecha de muerte"] >= (df_covid_death["Fecha de muerte"].max() - load_data_zone - pd.Timedelta('7 days')))
]


# In[60]:


df_covid_death_per_pop = df_covid_death_per_pop.groupby(["Código DIVIPOLA"]).count()["ID de caso"].reset_index()


# In[61]:


df_covid_death_per_pop = pd.merge(df_censo,df_covid_death_per_pop,on="Código DIVIPOLA", how="inner")


# In[62]:


df_covid_death_per_pop["death_per_pop"] = df_covid_death_per_pop["ID de caso"]*1e5/df_covid_death_per_pop["Población total"]


# In[63]:


df_select_table = df_covid_death_per_pop.loc[(df_covid_death_per_pop["Población total"]>50000)].sort_values("death_per_pop", ascending=False)


# In[64]:


color_list = list(((df_select_table["death_per_pop"].head(10).astype(int)/(df_select_table["death_per_pop"].head(10).astype(int)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Purples'][x]))


# In[65]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Población', 'Muertes semana %s a %s por 100K' % (current_week_min,current_week_max)]),
                 columnwidth = [70,60,90],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"].head(10) + ", " + df_select_table["NOMBRE DEPARTAMENTO"].head(10),
                     df_select_table["Población total"].head(10),
                     df_select_table["death_per_pop"].head(10).astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)',color_list])
                ))
            ])
fig.update_layout(height=450, title_text="Municipios con más muertes por 100.000 habitantes en la última semana antes de rezago",showlegend=False)
l_charts.append(fig)


# In[66]:


df_select_table = df_covid_death_per_pop.sort_values("Población total", ascending=False).head(25).sort_values("death_per_pop", ascending=False)


# In[67]:


color_list = list(((df_select_table["death_per_pop"].head(10).astype(int)/(df_select_table["death_per_pop"].head(10).astype(int)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Purples'][x]))


# In[68]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Población', 'Muertes semana %s a %s por 100K' % (current_week_min,current_week_max)]),
                 columnwidth = [70,60,90],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"] + ", " + df_select_table["NOMBRE DEPARTAMENTO"],
                     df_select_table["Población total"],
                     df_select_table["death_per_pop"].astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)',color_list])
                ))
            ])
fig.update_layout(height=750, title_text="Muertes por 100.000 habitantes en los principales municipios en la última semana antes de rezago",showlegend=False)
l_charts.append(fig)


# In[69]:


df_covid_cases_load = df_covid_cases_load.groupby(["week","Código DIVIPOLA"]).count()["ID de caso"].reset_index()


# In[70]:


df_covid_cases_current_week = df_covid_cases_load.loc[df_covid_cases_load["week"]=="current_week"]
df_covid_cases_previous_week = df_covid_cases_load.loc[df_covid_cases_load["week"]=="previous_week"]


# In[71]:


df_diff_cases = pd.merge(df_covid_cases_current_week,df_covid_cases_previous_week,on="Código DIVIPOLA", how="inner")[["Código DIVIPOLA","ID de caso_x","ID de caso_y"]].rename(columns={"ID de caso_x":"current_week","ID de caso_y":"previous_week"})


# In[72]:


df_diff_cases = pd.merge(df_censo,df_diff_cases,on="Código DIVIPOLA", how="inner")


# In[73]:


#df_diff_cases["current_week"] = df_diff_cases["current_week"]*1e5/df_diff_cases["Población total"]
#df_diff_cases["previous_week"] = df_diff_cases["previous_week"]*1e5/df_diff_cases["Población total"]


# In[74]:


df_diff_cases["diff"] = df_diff_cases["current_week"]*1e5/df_diff_cases["Población total"] - df_diff_cases["previous_week"]*1e5/df_diff_cases["Población total"]


# In[75]:


df_select_table = df_diff_cases.loc[(df_diff_cases["Población total"]>50000) & (df_diff_cases["diff"]<0)].sort_values("diff")


# In[76]:


color_list = list(((df_select_table["diff"].head(10).astype(int)*(-1)/(df_select_table["diff"].head(10).astype(int)*(-1)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Blues'][x-1]))


# In[77]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Semana %s a %s' % (current_week_min,current_week_max), 'Semana %s a %s' % (previous_week_min,previous_week_max), 'Cambio por 100K']),
                 columnwidth = [100,50,50,50],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"].head(10) + ", " + df_select_table["NOMBRE DEPARTAMENTO"].head(10),
                     df_select_table["current_week"].head(10),
                     df_select_table["previous_week"].head(10),
                     df_select_table["diff"].head(10).astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)','rgb(245, 245, 245)',color_list])
                ))
            ])
fig.update_layout(height=450, title_text="Municipios con mayor descenso de casos por 100.000 habitantes en las últimas semanas antes de rezago",showlegend=False)
l_charts.append(fig)


# In[78]:


df_select_table = df_diff_cases.loc[(df_diff_cases["Población total"]>50000) & (df_diff_cases["diff"]>0)].sort_values("diff", ascending=False)


# In[79]:


color_list = list(((df_select_table["diff"].head(10).astype(int)/(df_select_table["diff"].head(10).astype(int)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Reds'][x]))


# In[80]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Semana %s a %s' % (current_week_min,current_week_max), 'Semana %s a %s' % (previous_week_min,previous_week_max), 'Cambio por 100K']),
                 columnwidth = [100,50,50,50],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"].head(10) + ", " + df_select_table["NOMBRE DEPARTAMENTO"].head(10),
                     df_select_table["current_week"].head(10),
                     df_select_table["previous_week"].head(10),
                     df_select_table["diff"].head(10).astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)','rgb(245, 245, 245)',color_list])
                ))
            ])
fig.update_layout(height=450, title_text="Municipios con mayor aumento de casos por 100.000 habitantes en las últimas semanas antes de rezago",showlegend=False)
l_charts.append(fig)


# In[81]:


df_covid_death_load = df_covid_death.loc[
    (df_covid_death["Fecha de muerte"] < (df_covid_death["Fecha de muerte"].max() - load_data_zone)) &
    (df_covid_death["Fecha de muerte"] >= (df_covid_death["Fecha de muerte"].max() - load_data_zone - pd.Timedelta('14 days')))
]

df_covid_death_load["week"] = df_covid_death_load["Fecha de muerte"].apply(lambda x:"current_week" if (x > (df_covid_death_load["Fecha de muerte"].max()-pd.Timedelta('7 days'))) else "previous_week")


# In[82]:


current_week_max = datetime.datetime.strftime(df_covid_death_load.loc[df_covid_death_load["week"]=="current_week"]["date"].max(), '%d-%m')
current_week_min = datetime.datetime.strftime(df_covid_death_load.loc[df_covid_death_load["week"]=="current_week"]["date"].min(), '%d-%m')
previous_week_max = datetime.datetime.strftime(df_covid_death_load.loc[df_covid_death_load["week"]=="previous_week"]["date"].max(), '%d-%m')
previous_week_min = datetime.datetime.strftime(df_covid_death_load.loc[df_covid_death_load["week"]=="previous_week"]["date"].min(), '%d-%m')


# In[83]:


df_covid_death_load = df_covid_death_load.groupby(["week","Código DIVIPOLA"]).count()["ID de caso"].reset_index()


# In[84]:


df_covid_death_current_week = df_covid_death_load.loc[df_covid_death_load["week"]=="current_week"]
df_covid_death_previous_week = df_covid_death_load.loc[df_covid_death_load["week"]=="previous_week"]


# In[85]:


df_diff_death = pd.merge(df_covid_death_current_week,df_covid_death_previous_week,on="Código DIVIPOLA", how="inner")[["Código DIVIPOLA","ID de caso_x","ID de caso_y"]].rename(columns={"ID de caso_x":"current_week","ID de caso_y":"previous_week"})


# In[86]:


df_diff_death = pd.merge(df_censo,df_diff_death,on="Código DIVIPOLA", how="inner")


# In[87]:


df_diff_death["diff"] = df_diff_death["current_week"]*1e5/df_diff_death["Población total"] - df_diff_death["previous_week"]*1e5/df_diff_death["Población total"]


# In[88]:


df_select_table = df_diff_death.loc[(df_diff_death["Población total"]>50000) & (df_diff_death["diff"]<0)].sort_values("diff")


# In[89]:


color_list = list(((df_select_table["diff"].head(10).astype(int)*(-1)/(df_select_table["diff"].head(10).astype(int)*(-1)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Blues'][x-1]))


# In[90]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Semana %s a %s' % (current_week_min,current_week_max), 'Semana %s a %s' % (previous_week_min,previous_week_max), 'Cambio por 100K']),
                 columnwidth = [100,50,50,50],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"].head(10) + ", " + df_select_table["NOMBRE DEPARTAMENTO"].head(10),
                     df_select_table["current_week"].head(10),
                     df_select_table["previous_week"].head(10),
                     df_select_table["diff"].head(10).astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)','rgb(245, 245, 245)',color_list])
                ))
            ])
fig.update_layout(height=450, title_text="Municipios con mayor descenso de muertes por 100.000 habitantes en las últimas semanas antes de rezago",showlegend=False)
l_charts.append(fig)


# In[91]:


df_select_table = df_diff_death.loc[(df_diff_death["Población total"]>50000) & (df_diff_death["diff"]>0)].sort_values("diff", ascending=False)


# In[92]:


color_list = list(((df_select_table["diff"].head(10).astype(int)/(df_select_table["diff"].head(10).astype(int)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Reds'][x]))


# In[93]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Semana %s a %s' % (current_week_min,current_week_max), 'Semana %s a %s' % (previous_week_min,previous_week_max), 'Cambio por 100K']),
                 columnwidth = [100,50,50,50],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"].head(10) + ", " + df_select_table["NOMBRE DEPARTAMENTO"].head(10),
                     df_select_table["current_week"].head(10),
                     df_select_table["previous_week"].head(10),
                     df_select_table["diff"].head(10).astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)','rgb(245, 245, 245)',color_list])
                ))
            ])
fig.update_layout(height=450, title_text="Municipios con mayor aumento de muertes por 100.000 habitantes en las últimas semanas antes de rezago",showlegend=False)
l_charts.append(fig)


# In[94]:


df_select_table = df_diff_cases.sort_values("Población total", ascending=False).head(25).sort_values("diff")


# In[95]:


color_list_neg = list(((df_select_table["diff"].loc[df_select_table["diff"]<0].astype(int)*(-1)/(df_select_table["diff"].loc[df_select_table["diff"]<0].astype(int)*(-1)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Blues'][x]))


# In[96]:


color_list_pos = list(((df_select_table["diff"].loc[df_select_table["diff"]>=0].astype(int)/(df_select_table["diff"].loc[df_select_table["diff"]>=0].astype(int)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Reds'][x]))


# In[97]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Semana %s a %s' % (current_week_min,current_week_max), 'Semana %s a %s' % (previous_week_min,previous_week_max), 'Cambio por 100K']),
                 columnwidth = [100,50,50,50],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"] + ", " + df_select_table["NOMBRE DEPARTAMENTO"],
                     df_select_table["current_week"],
                     df_select_table["previous_week"],
                     df_select_table["diff"].astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)','rgb(245, 245, 245)',color_list_neg+color_list_pos])
                ))
            ])
fig.update_layout(height=800, title_text="Cambio de casos por 100K habitantes para semanas antes de rezago",showlegend=False)
l_charts.append(fig)


# In[98]:


df_select_table = df_diff_death.sort_values("Población total", ascending=False).head(25).sort_values("diff")


# In[99]:


color_list_neg = list(((df_select_table["diff"].loc[df_select_table["diff"]<0].astype(int)*(-1)/(df_select_table["diff"].loc[df_select_table["diff"]<0].astype(int)*(-1)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Blues'][x]))


# In[100]:


color_list_pos = list(((df_select_table["diff"].loc[df_select_table["diff"]>=0].astype(int)/(df_select_table["diff"].loc[df_select_table["diff"]>=0].astype(int)).max())*5).astype(int).apply(lambda x:cl.flipper()['seq']['9']['Reds'][x]))


# In[101]:


fig = go.Figure(data=[go.Table(header=dict(values=['Municipio', 'Semana %s a %s' % (current_week_min,current_week_max), 'Semana %s a %s' % (previous_week_min,previous_week_max), 'Cambio por 1M']),
                 columnwidth = [100,50,50,50],
                 cells=dict(values=[
                     df_select_table["NOMBRE MUNICIPIO"] + ", " + df_select_table["NOMBRE DEPARTAMENTO"],
                     df_select_table["current_week"],
                     df_select_table["previous_week"],
                     (df_select_table["diff"]*10).astype(int)
                 ],
                 align=['left', 'center', 'center', 'center'],
                 fill = dict(color=['rgb(245, 245, 245)','rgb(245, 245, 245)','rgb(245, 245, 245)',color_list_neg+color_list_pos])
                ))
            ])
fig.update_layout(height=800, title_text="Cambio de muertes por 1M habitantes para semanas antes de rezago",showlegend=False)
l_charts.append(fig)


# In[102]:


with open('index.html', 'w') as f:
    for chart in l_charts:
        f.write(chart.to_html(full_html=False, include_plotlyjs='cdn'))


# In[103]:


l_charts[0].write_image("case_main.png")


# In[104]:


l_charts[2].write_image("death_main.png")


# In[105]:


l_charts[4].write_image("peak.png")


# In[106]:


l_charts[6].write_image("most_cases.png")


# In[107]:


l_charts[-2].write_image("cases_diff.png")


# In[108]:


l_charts[-1].write_image("deaths_diff.png")

