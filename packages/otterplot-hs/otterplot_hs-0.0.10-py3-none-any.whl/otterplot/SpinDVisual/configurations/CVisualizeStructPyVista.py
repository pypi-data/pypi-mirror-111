r"""
Module which visualizes the spin lattice with pyvista
"""
import pyvista as pv
import pandas as pd
import numpy as np
from pathlib import Path


class CVisualizeStructPyVista:
    r"""
    Class for visualizing 1D domain wall
    """

    def __init__(self, file: Path, tiplength: float = 1.0, tipradius: float = 0.35, arrowscale: float = 0.7, offscreen: bool = False) -> None:
        r"""
        Initializes the the visualization

        Args:
            file(Path): STM file
            tiplength(float): geometry of arrow: tiplength
            tipradius(float): geometry of arrow: tipradius
            arrowscale(float): geometry of arrow: arrowscale
        """
        self.file = file
        df = pd.read_csv(self.file, sep=r'\s+', usecols=[0, 1, 2, 3, 4, 5], names=['x', 'y', 'z', 'sx', 'sy', 'sz'])
        self.x = df['x'].to_numpy()
        self.y = df['y'].to_numpy()
        self.z = df['z'].to_numpy()
        self.sx = df['sx'].to_numpy()
        self.sy = df['sy'].to_numpy()
        self.sz = df['sz'].to_numpy()
        self.r = np.column_stack((self.x, self.y, self.z))
        self.s = np.column_stack((self.sx, self.sy, self.sz))
        self.offscreen = offscreen

        self.tiplength = tiplength
        self.tipradius = tipradius
        self.arrowscale = arrowscale

    def __call__(self) -> pv.Plotter:
        r"""
        Calls the visualization.

        Returns:
            the pyvista plot object.
        """
        geom = pv.Arrow(start=np.array([-self.arrowscale / 2.0, 0, 0]), tip_length=self.tiplength,
                        tip_radius=self.tipradius, scale=self.arrowscale)
        self.p = pv.Plotter(off_screen=self.offscreen, lighting='three lights')
        pv.set_plot_theme("ParaView")
        pv.rcParams['transparent_background'] = True
        self.p.set_background('white')
        structure_pd = pv.PolyData(self.r)
        structure_pd.vectors = self.s
        structure_pd['oop'] = self.sz
        structure_pd_glyphs = structure_pd.glyph(orient=True, scale=True, geom=geom)

        self.p.add_mesh(structure_pd_glyphs, scalars='oop', show_scalar_bar=False)

        def cam() -> None:
            print('Camera postion', self.p.camera_position)

        self.p.add_key_event('c', cam)
        return self.p

    def set_camera(self, cam: np.array) -> None:
        r"""
        Sets the camera of the plotter.
        """
        self.p.camera = cam


    def screenshot(self, name_screenshot: str = 'STM') -> None:
        r"""
        Takes a screenshot
        """
        self.p.ren_win.OffScreenRenderingOn()
        self.p.window_size=[4000,4000]
        self.p.screenshot(f'{name_screenshot}.png')
        self.p.ren_win.OffScreenRenderingOff()
