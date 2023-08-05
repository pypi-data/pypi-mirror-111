declare const Jupyter: IJupyter;

type NotebookMetadata = {
  bby?: {
    id: string;
    posterId?: string;
  };
};

type CellMetadata = {
  bby?: {
    id: string;
    posterSlotId?: string;
    posterQuizOptId?: string;
  };
};

interface ICell {
  metadata: CellMetadata;
  [key: string]: any;
}

interface INotebook {
  metadata: NotebookMetadata;
  get_cell: (index: number) => ICell;
  get_cells: () => ICell[];
  get_selected_cell: () => ICell;
  get_selected_index: () => number | null;
  focus_cell: () => void;
  [key: string]: any;
}

interface IJupyter {
  notebook: INotebook;
  [key: string]: any;
}
