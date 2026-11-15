"""Excel source-observation boundary for CODAL ingestion V1."""

from src.ingestion.excel.dto import (
    CellRange,
    CellRef,
    CellObservation,
    CellValueKind,
    ColumnObservation,
    Diagnostic,
    DiagnosticSeverity,
    HeaderAxisKind,
    HeaderAxisObservation,
    HeaderFragmentObservation,
    RowObservation,
    SourceArtifactObservation,
    StructureStatus,
    TableObservation,
    WorkbookDateSystem,
    WorkbookMetadataObservation,
    WorkbookObservation,
    WorksheetObservation,
    WorksheetVisibility,
)


from src.ingestion.excel.reader import (
    ExcelReaderConfig,
    ExcelSourceContractError,
    ExcelSourceReadError,
    read_excel_file,
    read_excel_source,
)

__all__ = [
    "ExcelReaderConfig",
    "ExcelSourceContractError",
    "ExcelSourceReadError",
    "read_excel_file",
    "read_excel_source",
    "CellRange",
    "CellRef",
    "CellObservation",
    "CellValueKind",
    "ColumnObservation",
    "Diagnostic",
    "DiagnosticSeverity",
    "HeaderAxisKind",
    "HeaderAxisObservation",
    "HeaderFragmentObservation",
    "RowObservation",
    "SourceArtifactObservation",
    "StructureStatus",
    "TableObservation",
    "WorkbookDateSystem",
    "WorkbookMetadataObservation",
    "WorkbookObservation",
    "WorksheetObservation",
    "WorksheetVisibility",
]
