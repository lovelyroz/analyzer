(analyzer) PS D:\Winprojects\analyzer> python -u src/scripts/excel_template_annotation_audit.py --max-color-cells 1 excel/parsian_periodic.xlsx > template_annotation_audit_retry.txt 2>&1; "EXIT_CODE=$LASTEXITCODE"; Get-Content template_annotation_audit_retry.txt -Tail 35
EXIT_CODE=1
  A357:B357: A357.top=medium, A357.bottom=medium, B357.top=medium, B357.bottom=medium, A357.left=medium, B357.right=medium
  J357:K357: J357.top=medium, J357.bottom=medium, K357.top=medium, K357.bottom=medium, K357.right=medium
  A358:B358: A358.top=medium, A358.bottom=medium, B358.top=medium, B358.bottom=medium, A358.left=medium, B358.right=medium
  J358:K358: J358.top=medium, J358.bottom=medium, K358.top=medium, K358.bottom=medium, K358.right=medium
  A372:B372: A372.top=medium, A372.bottom=medium, B372.top=medium, B372.bottom=medium, A372.left=medium, B372.right=medium
  C372:F372: C372.top=medium, C372.bottom=medium, D372.top=medium, D372.bottom=medium, E372.top=medium, E372.bottom=medium, F372.top=medium, F372.bottom=medium, C372.left=medium, F372.right=medium
  A382:B382: A382.top=medium, A382.bottom=medium, B382.top=medium, B382.bottom=medium, A382.left=medium, B382.right=medium
  C382:F382: C382.top=medium, C382.bottom=medium, D382.top=medium, D382.bottom=medium, E382.top=medium, E382.bottom=medium, F382.top=medium, F382.bottom=medium, C382.left=medium, F382.right=medium
  A391:B391: A391.top=medium, A391.bottom=medium, B391.top=medium, B391.bottom=medium, A391.left=medium, B391.right=medium
  C391:F391: C391.top=medium, C391.bottom=medium, D391.top=medium, D391.bottom=medium, E391.top=medium, E391.bottom=medium, F391.top=medium, F391.bottom=medium, C391.left=medium, F391.right=medium
  A401:B401: A401.top=medium, A401.bottom=medium, B401.top=medium, B401.bottom=medium, A401.left=medium, B401.right=medium
  C401:F401: C401.top=medium, C401.bottom=medium, D401.top=medium, D401.bottom=medium, E401.top=medium, E401.bottom=medium, F401.top=medium, F401.bottom=medium, C401.left=medium, F401.right=medium
  B407:E407: B407.top=medium, B407.bottom=medium, C407.top=medium, C407.bottom=medium, D407.top=medium, D407.bottom=medium, E407.top=medium, E407.bottom=medium, B407.left=medium, E407.right=medium
  A410:I410: A410.top=medium, A410.bottom=medium, B410.top=medium, B410.bottom=medium, C410.top=medium, C410.bottom=medium, D410.top=medium, D410.bottom=medium, E410.top=medium, E410.bottom=medium, F410.top=medium, F410.bottom=medium, G410.top=medium, G410.bottom=medium, H410.top=medium, H410.bottom=medium, I410.top=medium, I410.bottom=medium, A410.left=medium, I410.right=medium
  A411:I411: A411.top=medium, A411.bottom=medium, B411.top=medium, B411.bottom=medium, C411.top=medium, C411.bottom=medium, D411.top=medium, D411.bottom=medium, E411.top=medium, E411.bottom=medium, F411.top=medium, F411.bottom=medium, G411.top=medium, G411.bottom=medium, H411.top=medium, H411.bottom=medium, I411.top=medium, I411.bottom=medium, A411.left=medium, I411.right=medium
COLOR_ANNOTATIONS
python : Traceback (most recent call last):
At line:1 char:1
+ python -u src/scripts/excel_template_annotation_audit.py --max-color- ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError

  File "D:\Winprojects\analyzer\src\scripts\excel_template_annotation_audit.py", line 274, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File "D:\Winprojects\analyzer\src\scripts\excel_template_annotation_audit.py", line 270, in main
    return audit_workbook(args.workbook, max_color_cells=args.max_color_cells)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Winprojects\analyzer\src\scripts\excel_template_annotation_audit.py", line 230, in audit_workbook
    print(
  File "C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 12-15: character maps to <undefined>