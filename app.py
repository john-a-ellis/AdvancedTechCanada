#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Depedencies
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from stats_can import StatsCan
import dash_bootstrap_components as dbc
import datetime as dt
sc = StatsCan()


# In[2]:


sc = StatsCan(data_folder="Resources")


# # Preping Tech Use

# In[3]:


advance_tech_use_df = sc.table_to_df("27-10-0367-01")


# In[4]:


advance_tech_use_df.rename(columns={'North American Industry Classification System (NAICS)':'NAICS', 
                                    'REF_DATE': 'Date',
                                    'VALUE':'Percentage',
                                    'Advanced or emerging technologies': 'Advanced Technology'}, 
                          inplace=True)
advance_tech_use_df['Date'] = advance_tech_use_df['Date'].dt.year.astype(str)


# In[5]:


plot_data=advance_tech_use_df.groupby(['Date','GEO','NAICS','Enterprise size', 'Advanced Technology'], observed=False)['Percentage'].mean()


# In[6]:


tech_plot_data_df=pd.DataFrame(plot_data)


# In[7]:


tech_plot_data_df.info()


# In[8]:


tech_plot_data_df.reset_index(inplace=True)


# In[9]:


compare_tech_2022 = tech_plot_data_df[tech_plot_data_df['Date'] =='2022']
repeating_columns = [column for column in compare_tech_2022.columns if column not in ['Date', 'Percentage']]


# In[10]:


compare_tech_2017 = tech_plot_data_df[(tech_plot_data_df['Date'] == '2017') & (tech_plot_data_df[repeating_columns].isin(compare_tech_2022[repeating_columns].to_dict('list')).all(axis=1))]


# In[11]:


compare_2017_2022_df = pd.merge(compare_tech_2022, compare_tech_2017, 
                                left_on=['GEO', 'NAICS', 'Enterprise size', 'Advanced Technology'], 
                                right_on=['GEO', 'NAICS', 'Enterprise size', 'Advanced Technology'],
                                suffixes=('_2022','_2017'))


# In[12]:


tech_plot_data_df.dropna(inplace=True)


# In[13]:


tech_list = ['Artificial intelligence (AI)', 'Biotechnology',
             'Blockchain technologies', 'Clean technologies',
             'Design or information control technologies',
             'Geomatics or geospatial technologies',
             'Integrated Internet of Things (IoT) systems',
             'Material handling, supply chain or logistics technologies',
             'Nanotechnology', 'Other types of advanced technologies',
             'Processing or fabrication technologies',
             'Business intelligence technologies',
             'Security or advanced authentication systems',
             'Additive manufacturing', 'Virtual, mixed and augmented reality',
             'Quantum technology', 'Robotics']


# In[14]:


compare_2017_2022_df['YoY Chg']=compare_2017_2022_df['Percentage_2022']-compare_2017_2022_df['Percentage_2017']
compare_2017_2022_df['%YoY Chg']=(compare_2017_2022_df['Percentage_2022']-compare_2017_2022_df['Percentage_2017'])/compare_2017_2022_df['Percentage_2017']
compare_2017_2022_df.dropna(inplace = True)


# # Preping Reasons

# In[15]:


reason_not_used_df = sc.table_to_df("27-10-0368-01")


# In[16]:





# In[17]:


reason_not_used_df.rename(columns={'North American Industry Classification System (NAICS)':'NAICS', 
                                   'Reasons for not using advanced or emerging technologies':'Reason Not Adopted',
                                   'REF_DATE': 'Date',
                                   'VALUE': 'Percentage'}, 
                          inplace=True)
reason_not_used_df['Date'] = reason_not_used_df['Date'].dt.year.astype(str)


# In[18]:


plot_data=reason_not_used_df.groupby(['Date','GEO','NAICS','Enterprise size', 'Reason Not Adopted'], observed=False)['Percentage'].mean()


# In[19]:


reason_plot_data_df=pd.DataFrame(plot_data)


# In[20]:


reason_plot_data_df.reset_index(inplace=True)


# In[21]:


reason_plot_data_df.dropna(inplace=True)
reason_plot_data_df.info()


# In[27]:


app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server
markdown_reason = '''
#### Description

Percentage of enterprises that did not adopt or use advanced technologies for specific reasons, 
by North American Industry Classification System (NAICS) code and enterprise size, based on a one-year observation period. 
Reasons for not adopting or using advanced technologies include not being convinced of economic benefit; 
difficulty in obtaining financing; high cost of advanced technologies; investment not necessary for continuing operations; 
lack of technical skills required to support this type of investment; organizational culture too inflexible; 
decisions made by parent, affiliates or subsidiary businesses; lack of technical support or services (from consultants or vendors); 
lack of information regarding advanced technology; difficulty in integrating new advanced technologies with existing systems, standards, and processes;
other reasons for not adopting or using advanced technologies; and adoption or use of advanced technologies not applicable to this business’s activities.  
[Adapated from Statistics Canada Table: 27-10-0367-01 Released: 2024-04-30](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2710036701)  
*This does not constitute an endorsement by Statistics Canada of this product.*
'''
markdown_adoption = '''
#### Description  

Percentage of enterprises that used specific types of advanced or emerging technologies, by North American Industry Classification System (NAICS) code and 
enterprise size, based on a one-year observation period. Advanced technologies include material handling, supply chain or logistics technologies; design or 
information control technologies; processing or fabrication technologies; clean technologies; security or advanced authentication systems; 
business intelligence technologies; and other types of advanced technologies. Emerging technologies include nanotechnology, biotechnology, 
geomatics or geospatial technologies, artificial intelligence (AI), integrated Internet of Things (IoT) systems, blockchain technologies, 
and other types of emerging technologies.  
[Adapted from Statistics Canada Table: 27-10-0368-01 Released date: 2024-04-30](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2710036801)    
*This does not constitute an endorsement by Statistics Canada of this product.*
'''
app.layout = html.Div([
    
    html.H1(children='Technology Adoption in Canada', style={'textAlign':'center'}),
    dcc.Dropdown(reason_plot_data_df.GEO.unique(), 'Canada', id='dropdown-selection-geo'),
    dcc.Dropdown(reason_plot_data_df.NAICS.unique(),'Total, all surveyed industries', id= 'dropdown-selection-naics'),
    dcc.Dropdown(reason_plot_data_df['Enterprise size'].unique(), 'Total, all enterprise sizes', id = 'dropdown-selection-enterprisesize'),
   
    dcc.Graph(id='graph-4-content'),
    
    dcc.Graph(id='graph-2-content'),
    dcc.Markdown(children=markdown_adoption),
    dcc.Graph(id='graph-1-content'),
    dcc.Markdown(children=markdown_reason),
    dcc.Graph(id='graph-3-content'),
    html.Label('Technology: ', id= 'label-selection-technology'),
    dcc.Dropdown(tech_plot_data_df['Advanced Technology'].unique(), tech_list, id = 'dropdown-selection-technology', multi=True, ),
])

@callback(
    Output('graph-1-content', 'figure'),
    Output('graph-2-content', 'figure'),
    Output('graph-3-content', 'figure'),
    Output('graph-4-content', 'figure'),
    Input('dropdown-selection-geo', 'value'),
    Input('dropdown-selection-naics', 'value'),
    Input('dropdown-selection-enterprisesize', 'value'),
    Input('dropdown-selection-technology', 'value'),
    # Input('radio-selection-ref-date', 'value')
)
def update_graph(getgeo, getnaics, getsize, gettech):
    df1 = reason_plot_data_df.loc[(reason_plot_data_df.GEO==getgeo) &
                (reason_plot_data_df.NAICS == getnaics) & 
                    (reason_plot_data_df['Enterprise size'] == getsize) 
                    # (reason_plot_data_df.REF_DATE == getdate)
    ]
    df2 = tech_plot_data_df.loc[(tech_plot_data_df.GEO==getgeo) &
                (tech_plot_data_df.NAICS == getnaics) & 
                    (tech_plot_data_df['Enterprise size'] == getsize) &
                    (tech_plot_data_df['Advanced Technology'].isin(tech_list))
                    # (reason_plot_data_df.REF_DATE == getdate)
    ]
    df2 = df2.sort_values(by='Percentage', ascending=True)
    df3 = tech_plot_data_df.loc[(tech_plot_data_df.GEO==getgeo) &
                (tech_plot_data_df.NAICS == getnaics) & 
                    (tech_plot_data_df['Enterprise size'] == getsize) &
                    (tech_plot_data_df['Advanced Technology'].isin(gettech))
    ]
    df4 = compare_2017_2022_df.loc[(compare_2017_2022_df.GEO==getgeo) &
                (compare_2017_2022_df.NAICS == getnaics) & 
                    (compare_2017_2022_df['Enterprise size'] == getsize) &
                    (compare_2017_2022_df['Advanced Technology'].isin(gettech))
    ]
    df4 = df4.sort_values(by='YoY Chg', ascending=False)
    
    fig_1 = px.scatter(df1, 
                       y='Reason Not Adopted', 
                       x='Percentage', 
                       size='Percentage', 
                       color='Date', 
                       # color_discrete_sequence=["red", "green", "blue"],
                       title= f'Reasons for Not Adopted - {getgeo} - {getnaics}',
                       )
    fig_2 = px.bar(df2, 
                   y='Advanced Technology', 
                   x='Percentage', 
                   color='Date',
                   # color_discrete_sequence=["red", "green", "blue"],
                   title = f'Technologies Adopted - {getgeo} - {getnaics}',
                   height = 600,
                  )
    fig_3 = px.bar(df3, 
                   y='Percentage', 
                   x='Date', 
                   color='Advanced Technology', 
                   barmode='group',
                   title = f'Technologies Adopted Over Time - {getgeo} - {getnaics}',
                  ) 
    fig_4 = px.bar(df4,
                   y = 'Advanced Technology',
                   x = 'YoY Chg', 
                   color = 'Advanced Technology',
                   title = f'Technologies Adopted 2017 - 2022 Change - {getgeo} - {getnaics}',
                  ) 
    return fig_1, fig_2, fig_3, fig_4
    
if __name__ == '__main__':
    app.run(jupyter_mode='_none', debug=None)


# In[ ]:





# In[ ]:




