import numpy as np
import plotly.graph_objects as go

# ----------------------------
# Validators
# ----------------------------
def check_optype(Type: str):
    if Type not in ['put', 'call']:
        raise ValueError("Type must be 'put' or 'call'.")

def check_trtype(Trade: str):
    if Trade not in ['long', 'short']:
        raise ValueError("Trade must be 'long' or 'short'.")

def check_instrument(inst: str):
    if inst not in ['option', 'underlying']:
        raise ValueError("Instrument must be 'option' or 'underlying'.")

# ----------------------------
# Payoff functions
# ----------------------------
def payoff_option(x, Type, strike, premium, trade, n):
    """
    payoff of a single option leg (per contract count n)
    Convention:
      - long: pays premium, receives intrinsic at expiry
      - short: opposite
    """
    x = np.asarray(x)

    if Type == 'call':
        intrinsic = np.maximum(x - strike, 0.0)
    else:
        intrinsic = np.maximum(strike - x, 0.0)

    # long option payoff = intrinsic - premium
    y = intrinsic - premium

    # short => negate
    if trade == 'short':
        y = -y

    return y * n

def payoff_underlying(x, entry, trade, n):
    """
    payoff of underlying position
      long:  (x - entry) * n
      short: -(x - entry) * n
    """
    x = np.asarray(x)
    y = (x - entry)

    if trade == 'short':
        y = -y

    return y * n

# ----------------------------
# Labels
# ----------------------------
abb = {'call': 'Call', 'put': 'Put', 'long': 'Long', 'short': 'Short',
       'option': 'Option', 'underlying': 'Underlying'}

def Strategy_builder(
    spot_range=20,
    spot=100,
    Strategy=None,
    save=False,
    file='fig.html'
):
    if Strategy is None:
        Strategy = [
            # مثال: دارایی پایه (۱ سهم/واحد) لانگ از قیمت spot
            {'Instrument': 'underlying', 'Trade': 'long', 'Entry': spot, 'Contract': 1},

            # اختیارها
            {'Instrument': 'option', 'Type': 'call', 'Strike': 110, 'Trade': 'short', 'Premium': 2, 'Contract': 1},
            {'Instrument': 'option', 'Type': 'put',  'Strike': 95,  'Trade': 'short', 'Premium': 6, 'Contract': 1},
        ]

    # Price grid
    x = spot * np.arange(100 - spot_range, 101 + spot_range, 0.01) / 100

    # Compute leg payoffs
    y_list = []
    labels = []

    for leg in Strategy:
        inst = str(leg.get('Instrument', 'option')).lower()
        check_instrument(inst)

        trade = str(leg['Trade']).lower()
        check_trtype(trade)

        n = int(leg.get('Contract', 1))

        if inst == 'option':
            opt_type = str(leg['Type']).lower()
            check_optype(opt_type)

            strike = float(leg['Strike'])
            premium = float(leg.get('Premium', 0.0))

            y_leg = payoff_option(x, opt_type, strike, premium, trade, n)
            label = f"{n} {abb[trade]} {abb[opt_type]}  ST:{strike}  Pr:{premium}"

        else:  # underlying
            entry = float(leg.get('Entry', spot))
            y_leg = payoff_underlying(x, entry, trade, n)
            label = f"{n} {abb[trade]} {abb['underlying']}  Entry:{entry}"

        y_list.append(y_leg)
        labels.append(label)

    # Plot
    y_total = np.zeros_like(x, dtype=float)
    fig = go.Figure()

    for y_leg, label in zip(y_list, labels):
        fig.add_trace(go.Scatter(
            x=x, y=y_leg, mode='lines', name=label, opacity=0.5
        ))
        y_total += y_leg

    fig.add_trace(go.Scatter(
        x=x, y=y_total, mode='lines', name='Strategy', line_width=2, line=dict(color='black')
    ))

    # Spot marker
    fig.add_shape(
        type='line',
        x0=spot, y0=float(np.min(y_total)),
        x1=spot, y1=float(np.max(y_total)),
        line=dict(color='red', dash='dash'),
        name='spot price'
    )

    fig.update_layout(
        title='Strategy Builder',
        # xaxis_title='Spot Price',
        yaxis_title='Payoff',
        legend=dict(orientation='h', yanchor='bottom', y=-0.2),
        showlegend=True,
        plot_bgcolor='white',
        hovermode='x',
        hoverdistance=100,
        spikedistance=1000,
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
                x0=float(x[0]),
                y0=0,
                x1=float(x[-1]),
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