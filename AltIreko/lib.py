import maya.cmds as cmds


class IrekoData(object):
    def __init__(self, max_que_length):
        self.current_layer = 0
        self.selection_stack = [["AltIreko_top_level_object"]]
        self.max_que_length = max_que_length
        self.restart_flg = 1

    def add_layer(self, selections):
        if self.restart_flg:
            self.reset_stack()

        if len(self.selection_stack) != self.current_layer + 1:
            self.selection_stack = self.selection_stack[0:self.current_layer + 1]

        if len(self.selection_stack) == self.max_que_length:
            self.selection_stack.pop(0)
            self.current_layer -= 1

        self.selection_stack.append(selections)
        self.current_layer += 1

    def get_layer(self, is_undo):
        self.restart_flg = 0

        if self.current_layer == 0:
            print("Stack reach first")
            return None

        self.current_layer -= 1
        return self.selection_stack[self.current_layer]

    def reset_stack(self):
        print("reset_called")
        self.current_layer = 0
        self.selection_stack = [["AltIreko_top_level_object"]]
        self.restart_flg = 0

    def append_obj(self, item):
        if self.current_layer >= 1:
            for i in range(1, self.current_layer):
                self.selection_stack[i].append(item)


class IrekoLib(object):
    def __init__(self, data):
        self.data = data

    def dive_in_action(self):
        selected_items = cmds.ls(selection=True, uuid=True)
        self.data.add_layer(selected_items)

        # add isolate mode action
        current_view = self.get_active_view()
        cmds.editor(current_view, edit=True, mainListConnection='activeList', lockMainConnection=True)
        cmds.isolateSelect(current_view, ls=True)
        cmds.isolateSelect(current_view, state=True)

    def previous_action(self):
        cmds.select(clear=True)
        target_item_list = self.data.get_layer(False)
        if target_item_list is None:
            print("Can not redo anymore!!!")
            return

        if target_item_list[0] == "AltIreko_top_level_object":
            current_view = self.get_active_view()
            cmds.isolateSelect(current_view, state=False)
            return

        # add isolate mode action
        target_item_list = self.convert_uuid_to_obj_name(target_item_list)
        cmds.select(target_item_list)
        current_view = self.get_active_view()
        cmds.editor(current_view, edit=True, mainListConnection='activeList', lockMainConnection=True)
        cmds.isolateSelect(current_view, ls=True)
        cmds.isolateSelect(current_view, state=1)

    def show_all_action(self):
        self.data.add_layer(["AltIreko_top_level_object"])
        self.data.restart_flg = 1
        current_view = self.get_active_view()
        cmds.isolateSelect(current_view, state=0)

    def get_active_view(self):
        return cmds.paneLayout('viewPanes', q=True, pane1=True)

    def convert_uuid_to_obj_name(self, uuid_list):
        item_list = []
        for uuid in uuid_list:
            try:
                item_list.append(cmds.ls(uuid, long=True)[0])
            except:
                print("Not found such uuid object!!!")

        return item_list

    def add_new_obj(self):
        item = cmds.ls(selection=True, uuid=True)

        current_view = self.get_active_view()
        cmds.isolateSelect(current_view, addSelected=True)
        self.data.append_obj(item)
