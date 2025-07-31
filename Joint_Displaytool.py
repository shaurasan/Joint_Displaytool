import maya.cmds as cmds

class Joint_displayTool:
            
    WINDOW_NAME = "jointDisplayWindow"

    
    def __init__(self):

        self.selection = None
        self.change = False  # スライダーの変更を追跡するフラグ

        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME, window=True)

        self.create_ui()

    def show_Axis(self, *args):

        selected_joint = cmds.ls(sl = True, type="joint")

        if not selected_joint:
            cmds.warning("ジョイントが選択されていません")
            return
        
        count = 0

        for joint in selected_joint:
            if(cmds.getAttr(joint + ".displayLocalAxis") == 0):
                cmds.setAttr(joint + ".displayLocalAxis", 1)
                count += 1
        
        if count == 0:
            print("選択ジョイントの方向表示はすでにオフです。")

    def hide_Axis(self, *args):

        selected_joint = cmds.ls(sl = True, type="joint")

        if not selected_joint:
            cmds.warning("ジョイントが選択されていません")
            return
        
        count = 0

        for joint in selected_joint:
            if(cmds.getAttr(joint + ".displayLocalAxis") == 1):
                cmds.setAttr(joint + ".displayLocalAxis", 0)
                count += 1
        
        if count == 0:
            print("選択ジョイントの方向表示はすでにオンです。")
        
    def size_change(self, value):

        if self.change:
            return

        selected_joints = cmds.ls(sl=True, type="joint")
        if not selected_joints:
            cmds.warning("ジョイントが選択されていません。")
            return
        
        for joint in selected_joints:
            
            #ジョイントの表示サイズをvalueに変更
            cmds.setAttr(joint + ".radius", value)

    def update_slider(self, *args):

        selected_joints = cmds.ls(sl=True, type="joint")

        if selected_joints:
            first_joint = selected_joints[0]
            
            #ジョイントの表示サイズを取得
            joint_value = cmds.getAttr(first_joint + ".radius")        

            self.change = True                #UIの更新
            cmds.floatSliderGrp(self.slider, e = True, v = joint_value)

            #エラーが発生してもしなくても最後に行う
            self.change = False

    """
    def axis_slider(self, value):
        
        try:
            cmds.setAttr("jointDisplay.jointAxisSwitch", 2, force = True)
            cmds.setAttr("jointDisplay.axisSize", value)
        except ValueError:
            cmds.warning("シーンにジョイントが存在しません")
    """
    def select_hierarchy(self, *args):
        initial_selection = cmds.ls(sl = True, l = True)

        if not initial_selection:
            cmds.warning("オブジェクトが選択されていません")
            return
        
        for item in initial_selection:
            cmds.select(item, add = True, hierarchy = True)

    def window_close(self, *args):
        if self.selection:
            
            #scriptJobの停止 forceは保護されたジョブを削除できる
            cmds.scriptJob(kill = self.selection, force = True)
            self.selection = None

    def create_ui(self):

        self.window = cmds.window(self.WINDOW_NAME, title="ジョイントツール",
                                  widthHeight=(250, 300), tlb = True, s = False,
                                  cc = self.window_close)

        form = cmds.formLayout()

        main_column = cmds.columnLayout(adj = True)

        cmds.rowLayout(nc =2, cw2 = (110, 110), 
                       cat = [(1, "both", 5), (2, "both", 5)])

        cmds.button(label = "表示", bgc = (0, 0.25, 0), h = 50, c = self.show_Axis)
        cmds.button(label = "非表示", bgc = (0.25, 0, 0), h = 50, c = self.hide_Axis)

        cmds.setParent("..")

        cmds.separator(h = 20, style = "none")
        self.slider = cmds.floatSliderGrp(
            label = "表示サイズ",   #ラベル
            field = True,          #数値入力フィールド
            minValue = 0.1,        #最小値
            maxValue = 10.0,       #最大値
            value = 1.0,           #初期値
            step = 0.1,            #刻み幅   
            cw3 = (50, 50, 100),   #ラベル、フィールド、スライダー
            cc = self.size_change  #スライダーの値が変更されたら
        )

        """
        initial_axis = 1.0
        try:
            initial_axis = cmds.getAttr("jointDisplay.axisSize")
        #引数が間違っている際
        except ValueError:
            print("jointDisplayが見つからない")

        self.axis_slider_grp = cmds.floatSliderGrp(
            label = "方向の表示サイズ",
            field = True,
            minValue = 0.1,
            maxValue = 5.0,
            value = initial_axis,
            step = 0.1,
            columnWidth3 = (60, 50, 116),
            changeCommand = self.axis_slider
        )
        """
        cmds.separator(h = 20, style = "none")
        cmds.button(label = "階層の選択", h = 50, c = self.select_hierarchy)
        cmds.setParent("..")

        cmds.formLayout(form, e = True, af = [(main_column, "top", 10),
                                                (main_column, "left", 10),
                                                (main_column, "right", 10)]
                                                )

        self.update_slider()
        #指定イベント発生時にスクリプトを実行 string, script
        self.selection = cmds.scriptJob(e = ["SelectionChanged", self.update_slider],
                                        pro = True)

        cmds.showWindow(self.window)


excute = Joint_displayTool()


"""
選択ジョイントの方向表示/非表示
階層の選択
ジョイントの表示サイズを変更するスライダー
一階層上下するボタンとリネーム
数値入力で複数ジョイントを変更
ジョイントの方向表示のサイズを変更
"""