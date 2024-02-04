
# strategies Builder

A module for calculation and visualization of day trading option contracts has arrived.


## Call Package

Call strategies Builder

```bash
from StrategiesBuilder import Strategy_builder as SB
```
    




## Examples

Set each Trade Action in one Dict.
```python
Action_1 = {'Type': 'call', 'Strike': 215, 'Trade': 'long', 'Premium': 6}
Action_2 = {'Type': 'put' , 'Strike': 210, 'Trade': 'long', 'Premium': 3}
Action_3 = {'Type': 'call', 'Strike': 210, 'Trade': 'long', 'Premium': 9}
Action_4 = {'Type': 'put',  'Strike': 215, 'Trade': 'long', 'Premium': 10}
```
Combine all Actions to create your strategies

```python
Strategy = [Action_1, Action_2,Action_3,Action_4]

SB( spot       = 212,
    spot_range = 15 ,
    Strategy   = Strategy
    )
## Show The Diagram
```


## 🚀 About Me
Quantitative Derivatives Analyst
-> linkedin : https://www.linkedin.com/in/sajad-taj/



# Package Reference
I extracted the basic code from this source 
### https://github.com/hashabcd/opstrat