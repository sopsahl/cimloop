import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def helper_funcion(x: int,  y: int = 0) -> int:
    return x ** 2 + y

def generate_pd_table(rows, row_names):
    """
    Generates a pandas dataframe that is neatly displayable as a table in jupyyter notebook
    
    Parameters:
        rows (list of dict): List of dictionaries, where each dictionary represents a row.
        row_names (list of str): List of row labels (must match the number of rows).

    Returns:
        pd.DataFrame: table of given info
    """
    # Convert list of dictionaries to a DataFrame
    df = pd.DataFrame(rows, index=row_names)

    return df
    
    
def generate_latex_table(df, title="Table Title", caption="Table caption", label="table:1"):
    """
    Generate a LaTeX-formatted table from a list of dictionaries, using row names.

    Parameters:
        df (pd.DataFrame): table of info in a pandas dataframe
        title (str): Title of the table.
        caption (str): Caption for the table.
        label (str): Label for referencing in LaTeX.

    Returns:
        str: LaTeX code for the table.
    """

    # Generate LaTeX table code
    latex_table = df.to_latex(index=True, caption=caption, label=label, column_format="|l" + "|c" * len(df.columns) + "|")

    # Add title manually, as pandas doesn't support it
    latex_code = f"\\begin{{table}}[h]\n\\centering\n\\textbf{{{title}}}\n\n{latex_table}\n\\end{{table}}"

    return latex_code

def generate_histograms(bitwidth, std, sparsity=.5):
    """
    Creates a list of probabilities for quantized values. Meant to be used as value for
    histogram category in workload yaml file

    Parameters:
        bitwidth (int): number of bits you are quantizing to, i.e. 4/8
        std (float): std deviation to be applied to your normal distribution
        sparsity (float) (optional): what decimal sparsity to apply, i.e. 0.5 for 50%
    Returns:
        list<int>: list of probs.
    
    """
    num_bins = 2 ** (bitwidth - 1)
    bins = np.arange(0.5 - num_bins , num_bins+0.5) # add 0.5 for bin edges
    probs, _ = np.histogram(np.random.normal(0, std, 100000), bins=bins, density=True)
    
    # Apply sparsity (e.g., 50%)
    # Calculate scaling to make zero bin equal to desired sparsity
    total = np.sum(probs)
    zero_ix = num_bins -1
    current_zero = probs[zero_ix]
    desired_zero = sparsity * total
    scaling_factor = (total - desired_zero) / (total - current_zero)

    probs *= scaling_factor
    probs[zero_ix] = desired_zero  # Set center bin to exact value

    probs /= np.sum(probs)  # Normalize after redistributing mass
    print("new_changed")
    return probs.tolist()

def plot_energy_efficiency_vs_voltage(efficiencies,voltages):
    """
    Plots efficiences (TOPS/W) vs voltages (V)
    Parameters:
        efficiencies (dict(str,list)): dictionary of lists with keys designating the datapath used and value being a list
                                       of efficiency values. Only accepts keys in ["int8", "int4", "int4vsq"].
        voltages (list): list of voltages aligned with efficiency values
    returns:
        None (graph displayed)
    """
    for key in efficiencies.keys():
        assert key in ["int8", "int4", "int4vsq"]

    int8 = efficiencies["int8"] 
    int4 = efficiencies["int4"] 
    int4_vsq = efficiencies["int4vsq"]

    plt.figure(figsize=(8,6))
    plt.plot(voltages, int8, 'o-', label='INT8')
    plt.plot(voltages, int4, 's--', label='INT4')
    plt.plot(voltages, int4_vsq, 'd-.', label='INT4-VSQ')

    plt.xlabel('Voltage (V)')
    plt.ylabel('Energy Efficiency (TOPS/W)')
    plt.title('Energy Efficiency vs. Voltage')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()