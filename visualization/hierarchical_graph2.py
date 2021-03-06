from vtk import *

treeFileName = "itkModulesNoGroups.xml"
graphFileName = "itkIncludes.csv"

reader1 = vtkXMLTreeReader()
reader1.SetFileName(treeFileName)
reader1.SetEdgePedigreeIdArrayName("tree edge")
reader1.GenerateVertexPedigreeIdsOff()
reader1.SetVertexPedigreeIdArrayName("id")

stringfilter = vtkStringToNumeric()
stringfilter.SetInputConnection(reader1.GetOutputPort())

reader2 = vtkDelimitedTextReader()
reader2.SetFieldDelimiterCharacters(",")
reader2.SetFileName(graphFileName)

reader1.Update()
reader2.Update()

graph = vtkTableToGraph()
graph.AddInputConnection(reader2.GetOutputPort())
graph.AddLinkEdge("Field 0", "Field 1")

view = vtkHierarchicalGraphView()
# view.SetInteractionModeTo3D()
view.DisplayHoverTextOff()
view.SetLayoutStrategyToTree()
view.GetRenderWindow().SetMultiSamples(0)
view.SetHierarchyFromInputConnection(stringfilter.GetOutputPort())
view.SetGraphFromInputConnection(graph.GetOutputPort())
# view.SetVertexColorArrayName("VertexDegree")
view.SetVertexColorArrayName("colorId")
view.SetColorVertices(True)
view.SetVertexLabelArrayName("name")
view.SetVertexLabelVisibility(True)
view.SetScalingArrayName("TreeRadius")

view.Update()
#view.SetGraphEdgeColorArrayName("graph edge")
#view.SetColorGraphEdgesByArray(True)
view.SetBundlingStrength(0.9)

ct = vtkTreeLayoutStrategy()
view.SetLayoutStrategy(ct)
ct.SetRadial(True)
ct.SetAngle(360)
ct.SetLeafSpacing(0.5)
ct.SetLogSpacingValue(0.3)

theme = vtkViewTheme()
theme.SetLineWidth(1)
theme.SetCellColor(0.0, 0.0, 0.0)
theme.SetCellOpacity(0.1)
theme.GetPointTextProperty().SetColor(0.0, 0.0, 0.0)
theme.SetBackgroundColor(1.0, 1.0, 1.0)
theme.SetBackgroundColor2(1.0, 1.0, 1.0)
theme.SetOutlineColor(1.0, 1.0, 1.0)
view.ApplyViewTheme(theme)

view.GetRenderWindow().LineSmoothingOn()
view.GetRenderWindow().SetMultiSamples(4)
view.ResetCamera()

view.GetInteractor().Initialize()
view.GetInteractor().Start()
