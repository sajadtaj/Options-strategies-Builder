import numpy as np
import plotly.graph_objects as go

def check_optype(Type):
    if (Type not in ['put','call']):
        raise ValueError("Input 'put' for put and 'call' for call!")

def check_trtype(Trade):
    if (Trade not in ['long','short']):
        raise ValueError("Input 'long' for Buy and 'short' for Sell!")  

def payoff_calculator(x, Type, strike, Premium, Trade, n):
    y=[]
    if Type=='call':
        for i in range(len(x)):
            y.append(max((x[i]-strike-Premium),-Premium))
    else:
        for i in range(len(x)):
            y.append(max(strike-x[i]-Premium,-Premium))
    y=np.array(y)

    if Trade=='s':
        y=-y
    return y*n



abb = {'call': 'Call', 'put': 'Put', 'long': 'Long', 'short': 'Short'}

def Strategy_builder(
    spot_range=20,
    spot=100,
    Strategy=[
        {'Type':'call','Strike':110 ,'Trade':'short' ,'Premium':2 ,'Contract':1},
        {'Type':'put' ,'Strike':95  ,'Trade':'short' ,'Premium':6 ,'Contract':1}
    ],
    save=False,
    file='fig.html'
):

    x = spot * np.arange(100 - spot_range, 101 + spot_range, 0.01) / 100
    y0 = np.zeros_like(x)         
    
    y_list = []
    for op in Strategy:
        Type = str.lower(op['Type'])
        Trade = str.lower(op['Trade'])
        check_optype(Type)
        check_trtype(Trade)
        
        Strike = op['Strike']
        Premium = op['Premium']
        try:
            Contract = op['Contract']
        except:
            Contract = 1
        y_list.append(payoff_calculator(x, Type, Strike, Premium, Trade, Contract))
    
    def plotter():
        y = 0
        fig = go.Figure()
        for i in range(len(Strategy)):
            try:
                Contract = str(Strategy[i]['Contract'])  
            except:
                Contract = '1'
                
            label = Contract + ' ' + str(abb[Strategy[i]['Trade']]) + ' ' + str(abb[Strategy[i]['Type']]) + ' ST: ' + str(Strategy[i]['Strike'])
            fig.add_trace(go.Scatter(x=x, y=y_list[i], mode='lines', name=label, opacity=0.5))
            y += np.array(y_list[i])
        
        fig.add_trace(
            go.Scatter(
                x=x, 
                y=y,
                mode='lines',
                name='Strategy',
                line_width=2,
                line=dict(color='black')
                      ))
        fig.add_shape(type='line'
            , x0=spot
            , y0=np.min(y)
            , x1=spot
            , y1=np.max(y)
            , line=dict(color='red', dash='dash')
            , name='spot price')
        
        fig.update_layout(
            title='Options Strategy Builder',
            xaxis_title='Spot Price',
            yaxis_title='Payoff',
            legend=dict(orientation='h', yanchor='bottom', y=-0.2),
            showlegend=True,
            plot_bgcolor='white',
            hovermode='x',
            hoverdistance=100,  # Distance to show hover label of data point
            spikedistance=1000,  # Distance to show spike
        )
        fig.update_yaxes(zeroline=True, zerolinewidth=6, zerolinecolor='white')

        fig.update_xaxes(showspikes=True, spikethickness=1)
        fig.update_yaxes(showspikes=True, spikethickness=1)
        fig.add_hline(y=0, line_dash='dash', line_color='black')
        
        fig.update_layout(
            shapes=[
                dict(
                    type='rect',
                    xref='x',
                    yref='paper',
                    x0=x[0],
                    y0=0,
                    x1=x[-1],
                    y1=1,
                    fillcolor='grey',
                    opacity=0.1,
                    layer='below',
                    line_width=0,
                )
            ],
            annotations=[
                dict(
                    x=spot,
                    y=0,
                    xref='x',
                    yref='y',
                    text='Spot Price',
                    showarrow=True,
                    arrowhead=1,
                    ax=0,
                    ay=30,
                    font=dict(size=12),
                )
            ]
        )
        if save:
            fig.write_html(file)
        fig.show()

    plotter()