"""
Instruction:
    Copy this code to the first cell of the Jupyter notebook you want to run in the Google Colab. It automatically configures it for rendering.
"""
import sys, os
if 'google.colab' in sys.modules and not os.path.exists('.done'):
    !wget -q https://raw.githubusercontent.com/FredAmouzgar/python_Exercise/master/Colab_setup/setup_colab.sh -O- | bash
    !touch .done

# Creating a virtual display to draw game images on.
if type(os.environ.get("DISPLAY")) is not str or len(os.environ.get("DISPLAY")) == 0:
    !bash ../xvfb start
    os.environ['DISPLAY'] = ':1'
