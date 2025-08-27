import pandas as pd
import plotly.graph_objects as go

# Example dataset (replace with your full dataframe)

#df = pd.read_csv('../../data/synthetic_transactions_realistic_names.csv')

#synthetic_transactions_overlap
df = pd.read_csv('../../data/synthetic_with_noise.csv')



# Build list of unique nodes
nodes = list(pd.unique(df[["Originator_Name", "Beneficiary_Name"]].values.ravel()))

# Map node names to indices
node_indices = {name: i for i, name in enumerate(nodes)}

# Build source, target, value arrays
sources = [node_indices[o] for o in df["Originator_Name"]]
targets = [node_indices[b] for b in df["Beneficiary_Name"]]
values  = df["Amount"].tolist()

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes,
        color="lightblue"
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        hovertemplate='From %{source.label} → %{target.label}<br>Amount: %{value}<extra></extra>'
    )
)])

fig.update_layout(title_text="Interactive Transaction Flow", font_size=10)
fig.show()
