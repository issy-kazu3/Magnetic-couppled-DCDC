'2015/10/28  磁気結合型コンバータ向けﾘｱｸﾄﾙのインダクタンス計算スクリプト　コイルA電流,コイルB電流->La,Lb,Mabを算出 磁性材の非線形性を考慮

dim Turn,Cuh,Cut,Cucl,Cur,Clcnt,Clw,Clh,Icorew,Icoreh,Cll,Uwplus,Uhplus,Udepth,Usidew,Ang,Corecl	'プリミティブな値。これらからモデルが決まる。
dim Cur1,Cur2	'右、左コイルの電流　各々プラスで磁界が打ち消す方向に電流が流れるようにモデルを組む
dim leak1x,leak1z,leak2x,leak2z	'漏れ磁束計測用の座標　１がコイル1で、2がコイル2

dim Startedge,Icorecl,Uinw,Length,Ilength,Holelength,Coilw,Coilh,Uw,Uh	'1次的に計算される寸法
dim pi
pi=3.1415926535897932384626433832795028841971693993
dim ii
dim str	'文字列の入れ物
dim savepath	'ファイルのセーブするパス＆ファイル名
dim savedata	'出力する自己インダクタンス　相互インダクタンス算出結果のパス＆ファイル
dim saveflux	'磁束密度を出力するパス
'------------------ここが編集する部分-----------------------------------------------
savepath="D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\MAXWELL16_SCRIPT\25MODEL_DETAILED_COIL\Project1.aedt"	'ファイルのセーブするパス＆ファイル名
savedata="D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\MAXWELL16_SCRIPT\25MODEL_DETAILED_COIL\Project1_Maxwell3DDesign1.txt" '出力する自己インダクタンス　相互インダクタンス算出結果のパス＆ファイル
saveflux="D:\Userarea\J0125789\Documents\ANSYS_CAE\ANSOFT\MAXWELL\MAXWELL16_SCRIPT\25MODEL_DETAILED_COIL\"	'磁束密度を記録するpath

Cur1 = 100.0	'とりあえず100A
Cur2 = 50.0	'とりあえず50A

Turn=32	':ターン数（片側コイル)
Cuh=6.5	':銅線幅 
Cut=1.8	':銅線厚み 
Cucl=0.4	'コイル間のクリアランス
Cur=5	':コイル内径r
Clcnt=4	':コイル間中央の隙間
Clw=3.05	':コアコイル横側クリアランス
Clh=3.25	':コアコイル縦側クリアランス
Icorew=32	':Iコアの幅
Icoreh=25	':Iコアの高さ
Cll=3.56	':コイル前後のコアとの距離
Uwplus=0.6	':Uコア幅のIコア幅に対する差分
Uhplus=0.6	':Uコア高さのIコア高さに対する差分
Udepth=6	':Uコア凹の深さ
Usidew=20	':Uコア奥部分の横幅
Ang=20	':Uコア傾き部分の角度（全長方向の側面に対する曲り角度)
Corecl=0	'接着部分のクリアランス
'------------編集が必要な部分はここまで　以下は一切いじらなくてよい-------------------------------

Startedge=(Udepth+Usidew)*0.4	'折れ曲がる個所までのU側面長さ
Icorecl=Clcnt+Cuh*2+Clw*2	'Iコア間のクリアランス
Uinw=Icorecl-Uwplus		'Uコアの凹部の幅
Length=Turn*(Cut+Cucl)+Cll*2+Usidew*2	'コア全長
Ilength=Length-Udepth*2-Usidew*2	'Iコア全長
Holelength=Length-Usidew*2	'コア中央空間の前後長
Coilw=Icorew+Clw*2+Cuh*2	'コイルの横幅
Coilh=Icoreh+Clh*2+Cuh*2	'コイルの高さ
Coilinw=Icorew+Clw*2	'コイルの内部の横幅
Coilinh=Icoreh+Clh*2	'コイルの内部の高さ
Uw=Icorew+Uwplus		'Uコア幅（足の部分)
Uh=Icoreh+Uhplus		'Uコアの高さ（足の部分）

dim Icorer(3,2)		'Iコア　右　x,y,z * 始点/終点
dim Icorel(3,2)
dim Ucorefrr(3,2)	'Uコア　フロント　右キューブ
dim Ucorefrl(3,2)	'Uコア　フロント　左キューブ
dim Ucorefro(3,2)	'Uコア　フロント　奥キューブ
dim Ucorefrcorner(2)	'Uコア　フロント　Y屈曲開始、x屈曲終わり点
dim Ucorerrr(3,2)	'Uコア　リア　右キューブ
dim Ucorerrl(3,2)
dim Ucorerro(3,2)
dim Ucorerrcorner(2)

dim Coilinsweepctr(3,4)	'右コイル内側のｒ中心座標 最前方の端面　上右、上左、下右、下左
dim Coilinsweepline(3,2,4)'右コイル内側の4辺　最前方の端面　上右,上左、下右,下左、右上,右下、左上,左下

Icorer(1,1)=Icorecl/2
Icorer(1,2)=Icorecl/2+Icorew
Icorer(2,1)=Ilength/2*-1
Icorer(2,2)=Icorer(2,1)*-1
Icorer(3,1)=Icoreh/2*-1
Icorer(3,2)=Icorer(3,1)*-1

Icorel(1,1)=Icorer(1,1)*-1
Icorel(1,2)=Icorer(1,2)*-1
Icorel(2,1)=Icorer(2,1)
Icorel(2,2)=Icorer(2,2)
Icorel(3,1)=Icorer(3,1)
Icorel(3,2)=Icorer(3,2)

Ucorefrr(1,1)=Icorer(1,1)-Uwplus/2
Ucorefrr(1,2)=Icorer(1,2)+Uwplus/2
Ucorefrr(2,1)=Icorer(2,2)
Ucorefrr(2,2)=Icorer(2,2)+Udepth
Ucorefrr(3,1)=Icorer(3,1)-Uhplus/2
Ucorefrr(3,2)=Icorer(3,2)+Uhplus/2

Ucorefrl(1,1)=Ucorefrr(1,2)*-1
Ucorefrl(1,2)=Ucorefrr(1,1)*-1
Ucorefrl(2,1)=Ucorefrr(2,1)
Ucorefrl(2,2)=Ucorefrr(2,2)
Ucorefrl(3,1)=Ucorefrr(3,1)
Ucorefrl(3,2)=Ucorefrr(3,2)

Ucorefro(1,1)=Ucorefrl(1,1)
Ucorefro(1,2)=Ucorefrr(1,2)
Ucorefro(2,1)=Ucorefrl(2,2)
Ucorefro(2,2)=Ucorefro(2,1)+Usidew
Ucorefro(3,1)=Ucorefrl(3,1)
Ucorefro(3,2)=Ucorefrl(3,2)

Ucorefrcorner(1)=Ucorefrl(2,1)+Startedge	'傾斜開始y
Ucorefrcorner(2)=Ucorefrr(1,2)-(Ucorefro(2,2)-Ucorefrcorner(1))*tan(pi*Ang/180)	'傾斜終了x

Ucorerrr(1,1)=Ucorefrr(1,1)
Ucorerrr(1,2)=Ucorefrr(1,2)
Ucorerrr(2,1)=Ucorefrr(2,2)*-1
Ucorerrr(2,2)=Ucorefrr(2,1)*-1
Ucorerrr(3,1)=Ucorefrr(3,1)
Ucorerrr(3,2)=Ucorefrr(3,2)

Ucorerrl(1,1)=Ucorefrl(1,1)
Ucorerrl(1,2)=Ucorefrl(1,2)
Ucorerrl(2,1)=Ucorefrl(2,2)*-1
Ucorerrl(2,2)=Ucorefrl(2,1)*-1
Ucorerrl(3,1)=Ucorefrl(3,1)
Ucorerrl(3,2)=Ucorefrl(3,2)

Ucorerro(1,1)=Ucorefro(1,1)
Ucorerro(1,2)=Ucorefro(1,2)
Ucorerro(2,1)=Ucorefro(2,2)*-1
Ucorerro(2,2)=Ucorefro(2,1)*-1
Ucorerro(3,1)=Ucorefro(3,1)
Ucorerro(3,2)=Ucorefro(3,2)

Ucorerrcorner(1)=Ucorefrcorner(1)*-1	'傾斜開始y
Ucorerrcorner(2)=Ucorefrcorner(2)	'傾斜終了x

Coilinsweepctr(1,1)=Clcnt/2+Cuh+Coilinw-Cur	'x右上
Coilinsweepctr(2,1)=Turn/2*(Cut+Cucl)			'y右上
Coilinsweepctr(3,1)=Icoreh/2+Clh-Cur		'z右上
Coilinsweepctr(1,2)=Clcnt/2+Cuh+Cur		'x左上
Coilinsweepctr(2,2)=Turn/2*(Cut+Cucl)
Coilinsweepctr(3,2)=Icoreh/2+Clh-Cur
Coilinsweepctr(1,3)=Coilinsweepctr(1,1)		'x右下
Coilinsweepctr(2,3)=Coilinsweepctr(2,1)
Coilinsweepctr(3,3)=Coilinsweepctr(3,1)*-1
Coilinsweepctr(1,4)=Coilinsweepctr(1,2)		'x左下
Coilinsweepctr(2,4)=Coilinsweepctr(2,2)
Coilinsweepctr(3,4)=Coilinsweepctr(3,2)*-1

Coilinsweepline(1,1,1)=Coilinsweepctr(1,1)		'x始点　上
Coilinsweepline(2,1,1)=Coilinsweepctr(2,1)		'y始点　上
Coilinsweepline(3,1,1)=Coilinsweepctr(3,1)+Cur		'z始点　上
Coilinsweepline(1,2,1)=Coilinsweepctr(1,2)		'x終点　上
Coilinsweepline(2,2,1)=Coilinsweepctr(2,2)		'y終点　上
Coilinsweepline(3,2,1)=Coilinsweepctr(3,2)+Cur		'z終点　上
Coilinsweepline(1,1,2)=Coilinsweepctr(1,1)		'x始点　下
Coilinsweepline(2,1,2)=Coilinsweepctr(2,1)		'y始点　下
Coilinsweepline(3,1,2)=(Coilinsweepctr(3,1)+Cur)*-1		'z始点　下
Coilinsweepline(1,2,2)=Coilinsweepctr(1,2)		'x終点　下
Coilinsweepline(2,2,2)=Coilinsweepctr(2,2)		'y終点　下
Coilinsweepline(3,2,2)=(Coilinsweepctr(3,2)+Cur)*-1		'z終点　下
Coilinsweepline(1,1,3)=Coilinsweepctr(1,1)+Cur		'x始点　右
Coilinsweepline(2,1,3)=Coilinsweepctr(2,1)		'y始点　右
Coilinsweepline(3,1,3)=Coilinsweepctr(3,1)		'z始点　右
Coilinsweepline(1,2,3)=Coilinsweepctr(1,3)+Cur		'x終点　右
Coilinsweepline(2,2,3)=Coilinsweepctr(2,3)		'y終点　右
Coilinsweepline(3,2,3)=Coilinsweepctr(3,3)		'z終点　右
Coilinsweepline(1,1,4)=Coilinsweepctr(1,2)-Cur	'x始点　左
Coilinsweepline(2,1,4)=Coilinsweepctr(2,2)		'y始点　左
Coilinsweepline(3,1,4)=Coilinsweepctr(3,2)		'z始点　左
Coilinsweepline(1,2,4)=Coilinsweepctr(1,4)-Cur		'x終点　左
Coilinsweepline(2,2,4)=Coilinsweepctr(2,4)		'y終点　左
Coilinsweepline(3,2,4)=Coilinsweepctr(3,4)		'z終点　左


'-------------作図はここから---------------------------------------------

Dim oAnsoftApp
Dim oDesktop
Dim oProject
Dim oDesign
Dim oEditor
Dim oModule
Set oAnsoftApp = CreateObject("AnsoftMaxwell.MaxwellScriptInterface")
Set oDesktop = oAnsoftApp.GetAppDesktop()
oDesktop.RestoreWindow
Set oProject = oDesktop.NewProject
'Set oProject = oDesktop.SetActiveProject("Project1")
oProject.InsertDesign "Maxwell 3D", "Maxwell3DDesign1", "Magnetostatic", ""
Set oDesign = oProject.SetActiveDesign("Maxwell3DDesign1")
Set oEditor = oDesign.SetActiveEditor("3D Modeler")
'------------透磁率を微分透磁率に変更＆デフォルト化　(見かけ透磁率ではなく------------------------------------------
oDesign.SetDesignSettings Array("NAME:Design Settings Data", "Allow Material Override:=",  _
  false, "EnabledObjects:=", Array(), "ComputeIncrementalMatrix:=", true, "PerfectConductorThreshold:=",  _
  1E+030, "InsulatorThreshold:=", 1)
'-----------Iコア 右-----------------------------------------------------
oEditor.CreateBox Array("NAME:BoxParameters", "XPosition:=",Icorer(1,1)&"mm", "YPosition:=",  _
  Icorer(2,1)+Corecl&"mm", "ZPosition:=",  Icorer(3,1)&"mm", "XSize:=", Icorer(1,2)-Icorer(1,1)&"mm", "YSize:=", Icorer(2,2)-Icorer(2,1)-Corecl*2&"mm", "ZSize:=",  _
  Icorer(3,2)-Icorer(3,1)&"mm"), Array("NAME:Attributes", "Name:=", "Icorer", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)
'-----------Iコア 左-----------------------------------------------------
oEditor.CreateBox Array("NAME:BoxParameters", "XPosition:=",Icorel(1,1)&"mm", "YPosition:=",  _
  Icorel(2,1)+Corecl&"mm", "ZPosition:=",  Icorel(3,1)&"mm", "XSize:=", Icorel(1,2)-Icorel(1,1)&"mm", "YSize:=", Icorel(2,2)-Icorel(2,1)-Corecl*2&"mm", "ZSize:=",  _
  Icorel(3,2)-Icorel(3,1)&"mm"), Array("NAME:Attributes", "Name:=", "Icorel", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)
'-----------Uコア 前-----------------------------------------------------
'-----------Uコア足 右-----------------------------------------------------
oEditor.CreateBox Array("NAME:BoxParameters", "XPosition:=",Ucorefrr(1,1)&"mm", "YPosition:=",  _
  Ucorefrr(2,1)&"mm", "ZPosition:=",  Ucorefrr(3,1)&"mm", "XSize:=", Ucorefrr(1,2)-Ucorefrr(1,1)&"mm", "YSize:=", Ucorefrr(2,2)-Ucorefrr(2,1)&"mm", "ZSize:=",  _
  Ucorefrr(3,2)- Ucorefrr(3,1)&"mm"), Array("NAME:Attributes", "Name:=", "Ucorefrr", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)
'-----------Uコア足 左-----------------------------------------------------
oEditor.CreateBox Array("NAME:BoxParameters", "XPosition:=",Ucorefrl(1,1)&"mm", "YPosition:=",  _
  Ucorefrl(2,1)&"mm", "ZPosition:=",  Ucorefrl(3,1)&"mm", "XSize:=", Ucorefrl(1,2)-Ucorefrl(1,1)&"mm", "YSize:=", Ucorefrl(2,2)-Ucorefrl(2,1)&"mm", "ZSize:=",  _
  Ucorefrl(3,2)-Ucorefrl(3,1)&"mm"), Array("NAME:Attributes", "Name:=", "Ucorefrl", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)
'----------Uコア　奥------------------------------------------------------------
oEditor.CreatePolyline Array("NAME:PolylineParameters", "IsPolylineCovered:=", true, "IsPolylineClosed:=",  _
  true, Array("NAME:PolylinePoints", _
  Array("NAME:PLPoint", "X:=", Ucorefro(1,2)&"mm", "Y:=", Ucorefro(2,1)&"mm", "Z:=", Ucorefro(3,1)&"mm"),  _
  Array("NAME:PLPoint", "X:=", Ucorefro(1,2)&"mm", "Y:=", Ucorefrcorner(1)&"mm", "Z:=", Ucorefro(3,1)&"mm"),_
  Array("NAME:PLPoint", "X:=", Ucorefrcorner(2)&"mm", "Y:=", Ucorefro(2,2)&"mm", "Z:=", Ucorefro(3,1)&"mm"),_
  Array("NAME:PLPoint", "X:=", -1*Ucorefrcorner(2)&"mm", "Y:=",Ucorefro(2,2)&"mm", "Z:=", Ucorefro(3,1)&"mm"),_
  Array("NAME:PLPoint", "X:=",  Ucorefro(1,1)&"mm", "Y:=", Ucorefrcorner(1)&"mm", "Z:=",Ucorefro(3,1)&"mm"),_
  Array("NAME:PLPoint", "X:=", Ucorefro(1,1)&"mm", "Y:=",  Ucorefro(2,1)&"mm", "Z:=", Ucorefro(3,1)&"mm"),_
   Array("NAME:PLPoint", "X:=",Ucorefro(1,2)&"mm", "Y:=", Ucorefro(2,1)&"mm", "Z:=", Ucorefro(3,1)&"mm")),_
   Array("NAME:PolylineSegments", Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 0, "NoOfPoints:=", 2), Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 1, "NoOfPoints:=", 2), Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 2, "NoOfPoints:=", 2), Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 3, "NoOfPoints:=", 2), Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 4, "NoOfPoints:=", 2), Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 5, "NoOfPoints:=", 2)), Array("NAME:PolylineXSection", "XSectionType:=",  _
  "None", "XSectionOrient:=", "Auto", "XSectionWidth:=", "0mm", "XSectionTopWidth:=",  _
  "0mm", "XSectionHeight:=", "0mm", "XSectionNumSegments:=", "0", "XSectionBendType:=",  _
  "Corner")), Array("NAME:Attributes", "Name:=", "Ucorefr", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)

oEditor.SweepAlongVector Array("NAME:Selections", "Selections:=", "Ucorefr", "NewPartsModelFlag:=",  	_
	  "Model"), Array("NAME:VectorSweepParameters", "DraftAngle:=", "0deg", "DraftType:=",  _
	  "Natural", "CheckFaceFaceIntersection:=", false, "SweepVectorX:=", "0mm", "SweepVectorY:=",  _
	  "0mm", "SweepVectorZ:=", Uh&"mm")
oEditor.Unite Array("NAME:Selections", "Selections:=",  _
  "Ucorefr,Ucorefrr,Ucorefrl"  _ 
  ), Array("NAME:UniteParameters", "KeepOriginals:=", false)
'------------Uコア　後ろ--------------------------------------------------------------------------
oEditor.DuplicateMirror Array("NAME:Selections", "Selections:=",  _
  "Ucorefr", "NewPartsModelFlag:=", "Model"), Array("NAME:DuplicateToMirrorParameters", "DuplicateMirrorBaseX:=",  _
  "0mm", "DuplicateMirrorBaseY:=", "0mm", "DuplicateMirrorBaseZ:=", "0mm", "DuplicateMirrorNormalX:=",  _
  "0mm", "DuplicateMirrorNormalY:=", "-1mm", "DuplicateMirrorNormalZ:=", "0mm"), Array("NAME:Options", "DuplicateAssignments:=",  _
  false)
oEditor.ChangeProperty Array("NAME:AllTabs", Array("NAME:Geometry3DAttributeTab", Array("NAME:PropServers",  _
  "Ucorefr_1"), Array("NAME:ChangedProps", Array("NAME:Name", "Value:=", "Ucorerr"))))

'------------コイルのスイープラインの作成------------------------------------------------
oEditor.CreatePolyline Array("NAME:PolylineParameters", "IsPolylineCovered:=", true, "IsPolylineClosed:=",  _
  false, Array("NAME:PolylinePoints", Array("NAME:PLPoint", "X:=", Coilinsweepctr(1,1)+Cur&"mm", "Y:=", Coilinsweepctr(2,1)&"mm", "Z:=", Coilinsweepctr(3,1)&"mm")) _
, Array("NAME:PolylineSegments", Array("NAME:PLSegment", "SegmentType:=",  _
  "AngularArc", "StartIndex:=", 0, "NoOfPoints:=", 3, "NoOfSegments:=", "0", "ArcAngle:=",  _
  "90deg", "ArcCenterX:=", Coilinsweepctr(1,1)&"mm", "ArcCenterY:=", Coilinsweepctr(2,1)&"mm", "ArcCenterZ:=", Coilinsweepctr(3,1)&"mm", "ArcPlane:=", "ZX")) _
, Array("NAME:PolylineXSection", "XSectionType:=",  _
  "None", "XSectionOrient:=", "Auto", "XSectionWidth:=", "0mm", "XSectionTopWidth:=",  _
  "0mm", "XSectionHeight:=", "0mm", "XSectionNumSegments:=", "0", "XSectionBendType:=",  _
  "Corner")), Array("NAME:Attributes", "Name:=", "Polyline1", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)

oEditor.CreatePolyline Array("NAME:PolylineParameters", "IsPolylineCovered:=", true, "IsPolylineClosed:=",  _
  false, Array("NAME:PolylinePoints", Array("NAME:PLPoint", _
"X:=", Coilinsweepline(1,1,1)&"mm", "Y:=", Coilinsweepline(2,1,1)&"mm", "Z:=",Coilinsweepline(3,1,1)&"mm"),_
 Array("NAME:PLPoint",_
 "X:=", Coilinsweepline(1,2,1)&"mm", "Y:=", Coilinsweepline(2,2,1)&"mm", "Z:=", Coilinsweepline(3,2,1)&"mm"))_
, Array("NAME:PolylineSegments", Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 0, "NoOfPoints:=", 2)), Array("NAME:PolylineXSection", "XSectionType:=",  _
  "None", "XSectionOrient:=", "Auto", "XSectionWidth:=", "0mm", "XSectionTopWidth:=",  _
  "0mm", "XSectionHeight:=", "0mm", "XSectionNumSegments:=", "0", "XSectionBendType:=",  _
  "Corner")), Array("NAME:Attributes", "Name:=", "Polyline2", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)

oEditor.CreatePolyline Array("NAME:PolylineParameters", "IsPolylineCovered:=", true, "IsPolylineClosed:=",  _
  false, Array("NAME:PolylinePoints", Array("NAME:PLPoint", _
"X:=", Coilinsweepctr(1,2)&"mm", "Y:=", Coilinsweepctr(2,2)&"mm", "Z:=", Coilinsweepctr(3,2)+Cur&"mm")) _
, Array("NAME:PolylineSegments", Array("NAME:PLSegment", "SegmentType:=",  _
  "AngularArc", "StartIndex:=", 0, "NoOfPoints:=", 3, "NoOfSegments:=", "0", "ArcAngle:=",  _
  "90deg", "ArcCenterX:=", Coilinsweepctr(1,2)&"mm", "ArcCenterY:=", Coilinsweepctr(2,2)&"mm", "ArcCenterZ:=", Coilinsweepctr(3,2)&"mm", "ArcPlane:=", "ZX")) _
, Array("NAME:PolylineXSection", "XSectionType:=",  _
  "None", "XSectionOrient:=", "Auto", "XSectionWidth:=", "0mm", "XSectionTopWidth:=",  _
  "0mm", "XSectionHeight:=", "0mm", "XSectionNumSegments:=", "0", "XSectionBendType:=",  _
  "Corner")), Array("NAME:Attributes", "Name:=", "Polyline3", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)

oEditor.CreatePolyline Array("NAME:PolylineParameters", "IsPolylineCovered:=", true, "IsPolylineClosed:=",  _
  false, Array("NAME:PolylinePoints", Array("NAME:PLPoint", _
"X:=", Coilinsweepline(1,1,4)&"mm", "Y:=", Coilinsweepline(2,1,4)&"mm", "Z:=",Coilinsweepline(3,1,4)&"mm"),_
 Array("NAME:PLPoint",_
 "X:=", Coilinsweepline(1,2,4)&"mm", "Y:=", Coilinsweepline(2,2,4)&"mm", "Z:=", Coilinsweepline(3,2,4)&"mm"))_
, Array("NAME:PolylineSegments", Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 0, "NoOfPoints:=", 2)), Array("NAME:PolylineXSection", "XSectionType:=",  _
  "None", "XSectionOrient:=", "Auto", "XSectionWidth:=", "0mm", "XSectionTopWidth:=",  _
  "0mm", "XSectionHeight:=", "0mm", "XSectionNumSegments:=", "0", "XSectionBendType:=",  _
  "Corner")), Array("NAME:Attributes", "Name:=", "Polyline4", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)

oEditor.CreatePolyline Array("NAME:PolylineParameters", "IsPolylineCovered:=", true, "IsPolylineClosed:=",  _
  false, Array("NAME:PolylinePoints", Array("NAME:PLPoint", _
"X:=", Coilinsweepctr(1,4)-Cur&"mm", "Y:=", Coilinsweepctr(2,4)&"mm", "Z:=", Coilinsweepctr(3,4)&"mm")) _
, Array("NAME:PolylineSegments", Array("NAME:PLSegment", "SegmentType:=",  _
  "AngularArc", "StartIndex:=", 0, "NoOfPoints:=", 3, "NoOfSegments:=", "0", "ArcAngle:=",  _
  "90deg", "ArcCenterX:=", Coilinsweepctr(1,4)&"mm", "ArcCenterY:=", Coilinsweepctr(2,4)&"mm", "ArcCenterZ:=", Coilinsweepctr(3,4)&"mm", "ArcPlane:=", "ZX")) _
, Array("NAME:PolylineXSection", "XSectionType:=",  _
  "None", "XSectionOrient:=", "Auto", "XSectionWidth:=", "0mm", "XSectionTopWidth:=",  _
  "0mm", "XSectionHeight:=", "0mm", "XSectionNumSegments:=", "0", "XSectionBendType:=",  _
  "Corner")), Array("NAME:Attributes", "Name:=", "Polyline5", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)

oEditor.CreatePolyline Array("NAME:PolylineParameters", "IsPolylineCovered:=", true, "IsPolylineClosed:=",  _
  false, Array("NAME:PolylinePoints", Array("NAME:PLPoint", _
"X:=", Coilinsweepline(1,2,2)&"mm", "Y:=", Coilinsweepline(2,2,2)&"mm", "Z:=",Coilinsweepline(3,2,2)&"mm"),_
 Array("NAME:PLPoint",_
 "X:=", Coilinsweepline(1,1,2)&"mm", "Y:=", Coilinsweepline(2,1,2)&"mm", "Z:=", Coilinsweepline(3,1,2)&"mm"))_
, Array("NAME:PolylineSegments", Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 0, "NoOfPoints:=", 2)), Array("NAME:PolylineXSection", "XSectionType:=",  _
  "None", "XSectionOrient:=", "Auto", "XSectionWidth:=", "0mm", "XSectionTopWidth:=",  _
  "0mm", "XSectionHeight:=", "0mm", "XSectionNumSegments:=", "0", "XSectionBendType:=",  _
  "Corner")), Array("NAME:Attributes", "Name:=", "Polyline6", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)

oEditor.CreatePolyline Array("NAME:PolylineParameters", "IsPolylineCovered:=", true, "IsPolylineClosed:=",  _
  false, Array("NAME:PolylinePoints", Array("NAME:PLPoint", _
"X:=", Coilinsweepctr(1,3)&"mm", "Y:=", Coilinsweepctr(2,3)&"mm", "Z:=", Coilinsweepctr(3,3)-Cur&"mm")) _
, Array("NAME:PolylineSegments", Array("NAME:PLSegment", "SegmentType:=",  _
  "AngularArc", "StartIndex:=", 0, "NoOfPoints:=", 3, "NoOfSegments:=", "0", "ArcAngle:=",  _
  "90deg", "ArcCenterX:=", Coilinsweepctr(1,3)&"mm", "ArcCenterY:=", Coilinsweepctr(2,3)&"mm", "ArcCenterZ:=", Coilinsweepctr(3,3)&"mm", "ArcPlane:=", "ZX")) _
, Array("NAME:PolylineXSection", "XSectionType:=",  _
  "None", "XSectionOrient:=", "Auto", "XSectionWidth:=", "0mm", "XSectionTopWidth:=",  _
  "0mm", "XSectionHeight:=", "0mm", "XSectionNumSegments:=", "0", "XSectionBendType:=",  _
  "Corner")), Array("NAME:Attributes", "Name:=", "Polyline7", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)

oEditor.CreatePolyline Array("NAME:PolylineParameters", "IsPolylineCovered:=", true, "IsPolylineClosed:=",  _
  false, Array("NAME:PolylinePoints", Array("NAME:PLPoint", _
"X:=", Coilinsweepline(1,2,3)&"mm", "Y:=", Coilinsweepline(2,2,3)&"mm", "Z:=",Coilinsweepline(3,2,3)&"mm"),_
 Array("NAME:PLPoint",_
 "X:=", Coilinsweepline(1,1,3)&"mm", "Y:=", Coilinsweepline(2,1,3)&"mm", "Z:=", Coilinsweepline(3,1,3)&"mm"))_
, Array("NAME:PolylineSegments", Array("NAME:PLSegment", "SegmentType:=",  _
  "Line", "StartIndex:=", 0, "NoOfPoints:=", 2)), Array("NAME:PolylineXSection", "XSectionType:=",  _
  "None", "XSectionOrient:=", "Auto", "XSectionWidth:=", "0mm", "XSectionTopWidth:=",  _
  "0mm", "XSectionHeight:=", "0mm", "XSectionNumSegments:=", "0", "XSectionBendType:=",  _
  "Corner")), Array("NAME:Attributes", "Name:=", "Polyline8", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)
'-------------------------コイル1個の作成---------------------------------------------------------------
oEditor.CreateRectangle Array("NAME:RectangleParameters", "IsCovered:=", true, "XStart:=",  _
	  Coilinsweepctr(1,1)+Cur&"mm", "YStart:=", Coilinsweepctr(2,1)&"mm", "ZStart:=", Coilinsweepctr(3,1)&"mm", "Width:=", Cuh&"mm", "Height:=",  _
	  -1*Cut&"mm", "WhichAxis:=", "Z"), Array("NAME:Attributes", "Name:=", "Cu", "Flags:=",  _
	  "", "Color:=", "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=",  _
	  "Global", "UDMId:=", "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  	_
	  true)

oEditor.Unite Array("NAME:Selections", "Selections:=",  _
  "Polyline1,Polyline2,Polyline3,Polyline4,Polyline5,Polyline6,Polyline7,Polyline" & _ 
  "8"), Array("NAME:UniteParameters", "KeepOriginals:=", false)
oEditor.SweepAlongPath Array("NAME:Selections", "Selections:=", "Cu,Polyline1", "NewPartsModelFlag:=",  _
  "Model"), Array("NAME:PathSweepParameters", "DraftAngle:=", "0deg", "DraftType:=",  _
  "Natural", "CheckFaceFaceIntersection:=", false, "TwistAngle:=", "0deg")
'------------------------片側全コイルの作成------------------------------------------------------------------
oEditor.AssignMaterial Array("NAME:Selections", "Selections:=", "Cu"), Array("NAME:Attributes", "MaterialValue:=",  _
  "" & Chr(34) & "copper" & Chr(34) & "", "SolveInside:=", true)
oEditor.DuplicateAlongLine Array("NAME:Selections", "Selections:=", "Cu", "NewPartsModelFlag:=",  _
  "Model"), Array("NAME:DuplicateToAlongLineParameters", "CreateNewObjects:=", true, "XComponent:=",  _
  "0mm", "YComponent:=", -1*(Cut+Cucl)&"mm", "ZComponent:=", "0mm", "NumClones:=", "30"), Array("NAME:Options", "DuplicateAssignments:=",  _
  false)
oEditor.ChangeProperty Array("NAME:AllTabs", Array("NAME:Geometry3DAttributeTab", Array("NAME:PropServers",  _
  "Cu"), Array("NAME:ChangedProps", Array("NAME:Name", "Value:=", "Cu_0"))))

'------------------------片側コイルの完成------------------------------------------------------------------

oEditor.DuplicateMirror Array("NAME:Selections", "Selections:=",  _
  "Cu_0,Cu_1,Cu_2,Cu_3,Cu_4,Cu_5,Cu_6,Cu_7,Cu_8,Cu_9,Cu_10,Cu_11,Cu_12,Cu_14,Cu_13," & _ 
  "Cu_15,Cu_16,Cu_17,Cu_18,Cu_19,Cu_20,Cu_21,Cu_22,Cu_23,Cu_24,Cu_25,Cu_26,Cu_27," & _ 
  "Cu_28,Cu_29", "NewPartsModelFlag:=", "Model"), Array("NAME:DuplicateToMirrorParameters", "DuplicateMirrorBaseX:=",  _
  "0mm", "DuplicateMirrorBaseY:=", "0mm", "DuplicateMirrorBaseZ:=", "0mm", "DuplicateMirrorNormalX:=",  _
  "-1mm", "DuplicateMirrorNormalY:=", "0mm", "DuplicateMirrorNormalZ:=", "0mm"), Array("NAME:Options", "DuplicateAssignments:=",  _
  false)
'------------------------両側コイルの完成------------------------------------------------------------------

'---------------コア材の選定--------------------------
Set oDesign = oProject.SetActiveDesign("Maxwell3DDesign1")
Set oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.AssignMaterial Array("NAME:Selections", "AllowRegionDependentPartSelectionForPMLCreation:=",  _
  true, "AllowRegionSelectionForPMLCreation:=", true, "Selections:=",  _
  "Icorel,Icorer,Ucorefr,Ucorerr"), Array("NAME:Attributes", "MaterialValue:=",  _
  "" & Chr(34) & "steel_1008" & Chr(34) & "", "SolveInside:=", true, "ShellElement:=",  _
  false, "ShellElementThickness:=", "nan ", "IsMaterialEditable:=", true, "UseMaterialAppearance:=",  _
  false, "IsLightweight:=", false)

'-------解析空間の設定 名前はRegion 全長の5倍を1辺とする立方体------------------------------
oEditor.CreateBox Array("NAME:BoxParameters", "XPosition:=", -1*Length/2*5&"mm", "YPosition:=",  _
  -1*Length/2*5&"mm", "ZPosition:=",-1* Length/2*5&"mm", "XSize:=", Length*5&"mm", "YSize:=", Length*5&"mm", "ZSize:=",  _
  Length*5&"mm"), Array("NAME:Attributes", "Name:=", "Box1", "Flags:=", "", "Color:=",  _
  "(132 132 193)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global", "UDMId:=",  _
  "", "MaterialValue:=", "" & Chr(34) & "vacuum" & Chr(34) & "", "SolveInside:=",  _
  true)
oEditor.ChangeProperty Array("NAME:AllTabs", Array("NAME:Geometry3DAttributeTab", Array("NAME:PropServers",  _
  "Box1"), Array("NAME:ChangedProps", Array("NAME:Name", "Value:=", "Region"), Array("NAME:Display Wireframe", "Value:=",  _
  true), Array("NAME:Color", "R:=", 128, "G:=", 255, "B:=", 255))))






'------対称条件の設定-------------------
str="Icorer,Icorel,Ucorefr,Ucorerr "
for ii=1 to Turn
str=str & ",Cu_" & ii-1
next
for ii=1 to Turn
str=str & ",Cu_" & ii-1 &"_1"
next
str=str & ",Region"
oEditor.Split Array("NAME:Selections", "Selections:=",  _
  str, "NewPartsModelFlag:=", "Model"), Array("NAME:SplitToParameters", "SplitPlane:=",  _
  "XY", "WhichSide:=", "PositiveOnly", "SplitCrossingObjectsOnly:=", false, "DeleteInvalidObjects:=",  _
  true)
oEditor.Split Array("NAME:Selections", "Selections:=",  _
  str, "NewPartsModelFlag:=", "Model"), Array("NAME:SplitToParameters", "SplitPlane:=",  _
  "ZX", "WhichSide:=", "PositiveOnly", "SplitCrossingObjectsOnly:=", false, "DeleteInvalidObjects:=",  _
  true)
Set oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignSymmetry Array("NAME:Symmetry1", "Faces:=", Array(7600), "IsOdd:=",  _
  true)
oModule.AssignSymmetry Array("NAME:Symmetry2", "Faces:=", Array(7757), "IsOdd:=",  _
  false)

'-----------------コイルへのターミナル(面)作成--------------------------------
for ii =1 to Turn/2
oEditor.Section Array("NAME:Selections", "Selections:=", "Cu_"&(ii-1), "NewPartsModelFlag:=",  _
  "Model"), Array("NAME:SectionToParameters", "CreateNewObjects:=", true, "SectionPlane:=",  _
  "XY", "SectionCrossObject:=", false)
oEditor.SeparateBody Array("NAME:Selections", "Selections:=", "Cu_"&(ii-1)&"_Section1", "NewPartsModelFlag:=",  _
  "Model")
next
for ii =1 to Turn/2
oEditor.Section Array("NAME:Selections", "Selections:=", "Cu_"&(ii-1)&"_1", "NewPartsModelFlag:=",  _
  "Model"), Array("NAME:SectionToParameters", "CreateNewObjects:=", true, "SectionPlane:=",  _
  "XY", "SectionCrossObject:=", false)
oEditor.SeparateBody Array("NAME:Selections", "Selections:=", "Cu_"&(ii-1)&"_1_Section1", "NewPartsModelFlag:=",  _
  "Model")
next
'----------------電流の付与---------------------
for ii =1 to Turn/2
Set oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignCurrent Array("NAME:Current"&(ii), "Objects:=", Array( _
  "Cu_"&(ii-1)&"_Section1_Separate1"), "Current:=", Cur1&"A", "IsSolid:=", false, "Point out of terminal:=",  _
  false)
next
for ii =1 to Turn/2
Set oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignCurrent Array("NAME:Current"&(ii)&"_1", "Objects:=", Array( _
  "Cu_"&(ii-1)&"_Section1"), "Current:=", Cur1&"A", "IsSolid:=", false, "Point out of terminal:=",  _
  true)
next
for ii =1 to Turn/2
Set oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignCurrent Array("NAME:Current"&(ii+Turn), "Objects:=", Array( _
  "Cu_"&(ii-1)&"_1_Section1"), "Current:=", Cur2&"A", "IsSolid:=", false, "Point out of terminal:=",  _
  false)
next
for ii =1 to Turn/2
Set oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignCurrent Array("NAME:Current"&(ii+Turn)&"_1", "Objects:=", Array( _
  "Cu_"&(ii-1)&"_1_Section1_Separate1"), "Current:=", Cur2&"A", "IsSolid:=", false, "Point out of terminal:=",  _
  true)
next

'--------------コイルのグループ化--------------
dim Currentm()
redim Currentm(Turn)
Currentm(0)="NAME:MatrixEntry"
for ii=1 to Turn/2
Currentm(ii)=Array("NAME:MatrixEntry", "Source:=", "Current" & ii, "NumberOfTurns:=", "1")
next
for ii=1 to Turn/2
Currentm(ii+Turn/2)=Array("NAME:MatrixEntry", "Source:=", "Current" & ii+Turn, "NumberOfTurns:=", "1")
next
dim Group1()
redim Group1(6)

Group1(0)="NAME:MatrixGroup"
Group1(1)="GroupName:="
Group1(2)="Group1"
Group1(3)="NumberOfBranches:="
Group1(4)="1"
Group1(5)="Sources:="
str=""
for ii=1 to Turn/2
str=str & "Current" & ii & ","
next
'str=str & "Current" & Turn & """"
Group1(6)=str

dim Group2()
redim Group2(6)
Group2(0)="NAME:MatrixGroup"
Group2(1)="GroupName:="
Group2(2)="Group2"
Group2(3)="NumberOfBranches:="
Group2(4)="1"
Group2(5)="Sources:="
str=""
for ii=1 to Turn/2
str=str & "Current" & ii+Turn & ","
next
'str=str & "Current" & Turn*2 & """"
Group2(6)=str

Set oModule = oDesign.GetModule("MaxwellParameterSetup")

oModule.AssignMatrix Array("NAME:Matrix1",  Currentm, Array("NAME:MatrixGroup", Group1, Group2))

'-------磁束を計算する断面----------------------
oEditor.Section Array("NAME:Selections", "Selections:=", "Icorer", "NewPartsModelFlag:=",  _
  "Model"), Array("NAME:SectionToParameters", "CreateNewObjects:=", true, "SectionPlane:=",  _
  "ZX", "SectionCrossObject:=", false)
oEditor.Section Array("NAME:Selections", "Selections:=", "Icorel", "NewPartsModelFlag:=",  _
  "Model"), Array("NAME:SectionToParameters", "CreateNewObjects:=", true, "SectionPlane:=",  _
  "ZX", "SectionCrossObject:=", false)
oEditor.Section Array("NAME:Selections", "Selections:=", "Ucorefr", "NewPartsModelFlag:=",  _
  "Model"), Array("NAME:SectionToParameters", "CreateNewObjects:=", true, "SectionPlane:=",  _
  "YZ", "SectionCrossObject:=", false)
'------漏れ磁束を測るポイント コイルより10mm上方-------------------------------
leak1x=Icorer(1,1)+Icorew/2
leak1z=Coilh/2+10	'コイル高さ+10mm
leak2x=-1*(Icorer(1,1)+Icorew/2)
leak2z=Coilh/2+10	'コイル高さ+10mm
oEditor.CreatePoint Array("NAME:PointParameters", "PointX:=", leak1x&"mm", "PointY:=",  _
  "0mm", "PointZ:=", leak1z&"mm"), Array("NAME:Attributes", "Name:=", "Point1", "Color:=",  _
  "(132 132 193)")
oEditor.CreatePoint Array("NAME:PointParameters", "PointX:=", leak2x&"mm", "PointY:=",  _
  "0mm", "PointZ:=", leak2z&"mm"), Array("NAME:Attributes", "Name:=", "Point2", "Color:=",  _
  "(132 132 193)")

'------------解析条件の設定---------------------------------------------------------------------------
Set oModule = oDesign.GetModule("AnalysisSetup")
oModule.InsertSetup "Magnetostatic", Array("NAME:Setup1", "Enabled:=", true, "MaximumPasses:=",  _
  10, "MinimumPasses:=", 2, "MinimumConvergedPasses:=", 1, "PercentRefinement:=",  _
  30, "SolveFieldOnly:=", false, "PercentError:=", 1, "SolveMatrixAtLast:=",  _
  true, "PercentError:=", 1, "UseIterativeSolver:=", false, "RelativeResidual:=",  _
  1E-006, "ComputeForceDensity:=", false, "ComputePowerLoss:=", false, "NonLinearResidual:=",  _
  0.001, Array("NAME:MuHcOption", "MuNonLinearBH:=", true, "HcNonLinearBH:=", true, "ComputeHc:=",  _
  false))

'---------------------実行と結果の保存-------------------------------------------------------
oProject.SaveAs  _
  savepath & _ 
  "", true
Set oDesign = oProject.SetActiveDesign("Maxwell3DDesign1")
oDesign.AnalyzeAll
Set oModule = oDesign.GetModule("AnalysisSetup")
oModule.ExportSolnData "Setup1 : LastAdaptive", "Matrix1", true, "",  _
  savedata



Set oModule = oDesign.GetModule("FieldsReporter")
oModule.EnterQty "B"
oModule.CalcOp "ScalarY"
oModule.CalcOp "Smooth"
oModule.EnterSurf "Icorer_Section1"
oModule.CalcOp "Integrate"
oModule.EnterScalar 1
oModule.EnterSurf "Icorer_Section1"
oModule.CalcOp "Integrate"
oModule.CalcOp "/"
oModule.ClcEval "Setup1 : LastAdaptive", Array()
oModule.CalculatorWrite  _
  saveflux&"core_fluxr.txt", Array("Solution:=",  _
  "Setup1 : LastAdaptive"), Array()

Set oModule = oDesign.GetModule("FieldsReporter")
oModule.EnterQty "B"
oModule.CalcOp "ScalarY"
oModule.CalcOp "Smooth"
oModule.EnterSurf "Icorel_Section1"
oModule.CalcOp "Integrate"
oModule.EnterScalar 1
oModule.EnterSurf "Icorel_Section1"
oModule.CalcOp "Integrate"
oModule.CalcOp "/"
oModule.ClcEval "Setup1 : LastAdaptive", Array()
oModule.CalculatorWrite  _
  saveflux&"core_fluxl.txt", Array("Solution:=",  _
  "Setup1 : LastAdaptive"), Array()

Set oModule = oDesign.GetModule("FieldsReporter")
oModule.EnterQty "B"
oModule.CalcOp "ScalarX"
oModule.CalcOp "Smooth"
oModule.EnterSurf "Ucorefr_Section1"
oModule.CalcOp "Integrate"
oModule.EnterScalar 1
oModule.EnterSurf "Ucorefr_Section1"
oModule.CalcOp "Integrate"
oModule.CalcOp "/"
oModule.ClcEval "Setup1 : LastAdaptive", Array()
oModule.CalculatorWrite  _
  saveflux&"core_fluxu.txt", Array("Solution:=",  _
  "Setup1 : LastAdaptive"), Array()

oModule.EnterQty "B"
oModule.CalcOp "ScalarY"
oModule.CalcOp "Smooth"
oModule.EnterPoint "Point1"
oModule.CalcOp "Value"
oModule.ClcEval "Setup1 : LastAdaptive", Array()
oModule.CalculatorWrite  _
  saveflux&"leak_flux_ptr.txt", Array("Solution:=",  _
  "Setup1 : LastAdaptive"), Array()

oModule.EnterQty "B"
oModule.CalcOp "ScalarY"
oModule.CalcOp "Smooth"
oModule.EnterPoint "Point2"
oModule.CalcOp "Value"
oModule.ClcEval "Setup1 : LastAdaptive", Array()

oModule.CalculatorWrite  _
  saveflux&"leak_flux_ptl.txt", Array("Solution:=",  _
  "Setup1 : LastAdaptive"), Array()


oDesktop.Quit
WScript.Sleep 5000
