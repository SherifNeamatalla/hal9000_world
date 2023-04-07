// theme.d.ts
import '@material-ui/core/styles';

declare module '@material-ui/core/styles' {
  interface Palette {
    matrix: PaletteColor;
    agentsList: PaletteColor;
    agentState: PaletteColor;
    actions: PaletteColor;
  }

  interface PaletteOptions {
    matrix?: PaletteColorOptions;
    agentsList?: PaletteColorOptions;
    agentState?: PaletteColorOptions;
    actions?: PaletteColorOptions;
  }
}
