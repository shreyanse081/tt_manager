# Timetable Management Software - Semi Automated Approach to Timetable Design.
# Copyright (C) 2016  Aadesh Magare - aadeshmagare01@gmail.com, Abhijit A M - abhijit13@gmail.com, Sourabh Limbore - limboresourabh@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/python
import wx
import globaldata
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import TextEditMixin, ColumnSorterMixin
# from threading import Thread
# from wx.lib.pubsub import setuparg1
# from wx.lib.pubsub import pub

# class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
#     def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
#                  size=wx.DefaultSize, style=0):
#         """Constructor"""
#         wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
#         listmix.TextEditMixin.__init__(self)
class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, TextEditMixin, ColumnSorterMixin):
    def __init__(self, parent, id=-1, style=wx.LC_REPORT | wx.ALWAYS_SHOW_SB, size=(700, 400)):
        wx.ListCtrl.__init__(self, parent, id=-1, style=wx.LC_REPORT | wx.ALWAYS_SHOW_SB ,size=(700, 400))
        ListCtrlAutoWidthMixin.__init__(self)
        TextEditMixin.__init__(self)
        if parent.key == 'Teacher':
            ColumnSorterMixin.__init__(self, 4)
        else:
            ColumnSorterMixin.__init__(self, 3)

    def GetListCtrl(self):
        return self

class AutoWidthListCtrl2(wx.ListCtrl, ListCtrlAutoWidthMixin, TextEditMixin):
    def __init__(self, parent, id=-1, style=wx.LC_REPORT | wx.ALWAYS_SHOW_SB, size=(700, 400)):
        wx.ListCtrl.__init__(self, parent, id=-1, style=wx.LC_REPORT | wx.ALWAYS_SHOW_SB ,size=(700, 400))
        ListCtrlAutoWidthMixin.__init__(self)
        TextEditMixin.__init__(self)

class HelpWindow(wx.Dialog):
    def __init__(self, parent, size=(900,900), id=-1, title="Keyboard Shortcuts"):
        wx.Dialog.__init__(self, parent, id, title, size)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.list = AutoWidthListCtrl2(self)
        self.list.Show(True)
        self.list.InsertColumn(0, 'Keyboard Shortcut', width=wx.LIST_AUTOSIZE_USEHEADER)
        self.list.InsertColumn(1, 'Description', width=wx.LIST_AUTOSIZE_USEHEADER)

        self.list.Append(['CTRL + N', 'New Project'])
        self.list.Append(['CTRL + O', 'Open Project'])
        self.list.Append(['CTRL + S', 'Save'])
        self.list.Append(['CTRL + SHIFT + S', 'Save As'])
        self.list.Append(['CTRL + C', 'Copy Cell Content'])
        self.list.Append(['CTRL + X', 'Cut Cell Content'])
        self.list.Append(['CTRL + V', 'Paste Copied Content'])
        self.list.Append(['CTRL + M', 'Merge Selected Cells'])
        self.list.Append(['CTRL + U', 'Unmerge Selected Cells'])
        self.list.Append(['CTRL + Q', 'Quit Application'])

        self.closebutton = wx.Button(self, label="Close")        
        self.Bind(wx.EVT_BUTTON, self.Closed, self.closebutton)
        self.closebutton.SetFocus()
        self.mainSizer.Add(self.list, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)
        self.mainSizer.Add(self.closebutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(self.mainSizer)
        self.Bind(wx.EVT_CLOSE, self.Closed)


    def Closed(self, event):
        self.Destroy()

class WarningView(wx.Dialog):
    def __init__(self, parent, source, size=(900,900), id=-1, title="Warnings"):
        wx.Dialog.__init__(self, parent, id, title, size, style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER)
        self.parent = parent
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.list = AutoWidthListCtrl2(self)
        # self.list = wx.ListCtrl(self,id, style=wx.LC_REPORT, size=(900, 400))
        self.list.Show(True)
        self.list.InsertColumn(0, 'No', width=wx.LIST_AUTOSIZE)
        self.list.InsertColumn(1, 'Warnings', width=wx.LIST_AUTOSIZE)

        #get data from the file or get it from the list
        for i in range(len(source)):
            self.list.Append([i+1, source[i]])

        self.hh = wx.BoxSizer(wx.HORIZONTAL)
        self.okbutton = wx.Button(self, label="OK", id=wx.ID_OK)        
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

        self.delbutton = wx.Button(self, label="Remove")        
        self.Bind(wx.EVT_BUTTON, self.onDel, self.delbutton)

        self.refbutton = wx.Button(self, label="Refresh")        
        self.Bind(wx.EVT_BUTTON, self.onRefresh, self.refbutton)

        self.canbutton = wx.Button(self, wx.ID_CANCEL, label='Close')
        self.Bind(wx.EVT_BUTTON, self.onClosed, self.canbutton)

        self.hh.Add(self.okbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.hh.Add(self.delbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.hh.Add(self.refbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.mainSizer.Add(self.list, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)
        self.mainSizer.Add(self.hh, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(self.mainSizer)
        # self.Bind(wx.EVT_CLOSE, self.onClosed)
        self.okbutton.SetFocus()

        # self.list.EnsureVisible(-1)
        # self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        # self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        # t = self.list.GetSize()
        # self.list.SetSize(t)

    def onClosed(self, event):
        print 'Close pressed'
        self.Destroy()

    def onRefresh(self, event):
        res = self.parent.CheckActualConstraints()
        parent = self.parent
        self.Destroy()
        dlg = WarningView(self.parent, res)
        dlg.ShowModal()
        if hasattr(dlg, 'result'):
            parent.ReplaceFile(dlg.result)
    def get_selected_items(self, list_control):

        selection = []
        # start at -1 to get the first selected item
        current = -1
        while True:
            next = self.GetNextSelected(list_control, current)
            if next == -1:
                return selection
            selection.append(next)
            current = next

    def GetNextSelected(self, list_control, current):
        return list_control.GetNextItem(current,
                                wx.LIST_NEXT_ALL,
                                wx.LIST_STATE_SELECTED)
    def onDel(self, event):
        i = self.list.GetFirstSelected()
        self.list.DeleteItem(i)
        #for multiselect delete / doesnt work perfectly
        # selection = self.get_selected_items(self.list)
        # for i in selection:
        #     self.list.DeleteItem(i)

    def onOK(self, event):
        #repace contents of file with updated one
        n = self.list.GetItemCount()
        res = []
        for i in range(n):
            x = self.list.GetItem(i, 1).GetText()
            # print x
            res.append(x)
        self.result = '\n'.join(res)
        self.Destroy()

# class TestThread(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#         self.start()    # start the thread

#     def run(self):
#         dlg = MyProgressDialog()
#         dlg.ShowModal()

# class MyProgressDialog(wx.Dialog):

#     def __init__(self):
#         wx.Dialog.__init__(self, None, title="Progress")
#         self.count = 0
 
#         self.progress = wx.Gauge(self, range=10)
 
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(self.progress, 0, wx.EXPAND)
#         self.SetSizer(sizer)
#         pub.subscribe(self.UpdateProgress, "updatePro")
    
#     def UpdateProgress(self, msg):
#         self.count += 1 
#         if self.count >= 10:
#             self.Destroy()
#             return
#         self.progress.SetValue(self.count)

class ListView(wx.Dialog):
    def __init__(self, parent, size=(600,50), id=-1, title="Enter Values",key='', label1= " Name", label2= "Abbrevation"):
        wx.Dialog.__init__(self, parent, id, title, size=(500,500))
        self.title = title
        self.key = key
        self.label1 = label1
        self.label2 = label2
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        myData = {}
        Cindex = 0
        # self.list = wx.ListCtrl(self,id, style=wx.LC_REPORT|wx.SUNKEN_BORDER, size=(300, 400))
        self.list = AutoWidthListCtrl(self,id, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SORT_ASCENDING, size=(300, 400))

        self.list.Show(True)
        self.list.InsertColumn(0, key + label1, width=wx.LIST_AUTOSIZE_USEHEADER)
        self.list.InsertColumn(1, label2, width=wx.LIST_AUTOSIZE_USEHEADER)

        if key == '' :
            if label1 == "Teacher":
                if label2 == "Subject":
                    keys = globaldata.teacher_subject_map.keys()
                    for k in keys:
                        self.list.Append([k, globaldata.teacher_subject_map[k]])
                else:
                    keys = globaldata.teacher_class_map.keys()
                    for k in keys:
                        self.list.Append([k, globaldata.teacher_class_map[k]])                    
            else:
                keys = globaldata.venue_class_map.keys()
                for k in keys:
                    self.list.Append([k, globaldata.venue_class_map[k]])

        if key == "Teacher" :
            self.list.InsertColumn(2,"WeeklyMax Load", width=wx.LIST_AUTOSIZE_USEHEADER)
            self.list.InsertColumn(3,"DailyMax Load", width=wx.LIST_AUTOSIZE_USEHEADER)
            for i in range(len(globaldata.teacher_fullnames)):
                self.list.Append([globaldata.teacher_fullnames[i],globaldata.teacher_shortnames[i+1], globaldata.teacher_weeklymax[i], globaldata.teacher_dailymax[i]])
                myData[i] = (globaldata.teacher_fullnames[i],globaldata.teacher_shortnames[i+1], globaldata.teacher_weeklymax[i], globaldata.teacher_dailymax[i])
                self.list.SetItemData(i, i)

        if key == "Venue" :
            self.list.InsertColumn(2,"Capacity", width=wx.LIST_AUTOSIZE_USEHEADER)
            for i in range(len(globaldata.venue_fullnames)):
                self.list.Append([globaldata.venue_fullnames[i],globaldata.venue_shortnames[i+1],globaldata.venue_capacity[i]])
                myData[i] = (globaldata.venue_fullnames[i],globaldata.venue_shortnames[i+1], globaldata.venue_capacity[i])
                self.list.SetItemData(i, i)

        if key == "Class" :
            self.list.InsertColumn(2,"Capacity", width=wx.LIST_AUTOSIZE_USEHEADER)
            for i in range(len(globaldata.class_fullnames)):
                self.list.Append([globaldata.class_fullnames[i],globaldata.class_shortnames[i+1],globaldata.class_capacity[i]])
                myData[i] = (globaldata.class_fullnames[i],globaldata.class_shortnames[i+1], globaldata.class_capacity[i])
                self.list.SetItemData(i, i)

        if key == "Subject" :
            self.list.InsertColumn(2,"NoOfHours", width=wx.LIST_AUTOSIZE_USEHEADER)
            for i in range(len(globaldata.subject_fullnames)):
                self.list.Append([globaldata.subject_fullnames[i],globaldata.subject_shortnames[i+1],globaldata.subject_credits[i]])
                myData[i] = (globaldata.subject_fullnames[i],globaldata.subject_shortnames[i+1],globaldata.subject_credits[i])
                self.list.SetItemData(i, i)

        self.hh = wx.BoxSizer(wx.HORIZONTAL)
        self.okbutton = wx.Button(self, label="OK")        
        self.Bind(wx.EVT_BUTTON, self.onOK, self.okbutton)

        self.addbutton = wx.Button(self, label="Add")        
        self.Bind(wx.EVT_BUTTON, self.onAdd, self.addbutton)

        self.delbutton = wx.Button(self, label="Remove")        
        self.Bind(wx.EVT_BUTTON, self.onDel, self.delbutton)

        self.canbutton = wx.Button(self, wx.ID_CANCEL, label='Cancel')
        self.Bind(wx.EVT_BUTTON, self.onClosed, self.canbutton)
        # self.Bind(wx.EVT_CLOSE, self.onClosed)

        self.hh.Add(self.okbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.hh.Add(self.addbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.hh.Add(self.delbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.hh.Add(self.canbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.mainSizer.Add(self.list, 0, flag=wx.EXPAND|wx.ALIGN_CENTER)
        self.mainSizer.Add(self.hh, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(self.mainSizer)
        self.okbutton.SetFocus()
        self.list.itemDataMap = myData

        # self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list)


    # def OnColClick(self, evt):
    #     print 'col clicked'
    def onClosed(self, event):
        # print 'Close pressed'
        self.Destroy()

    def onDel(self, event):
        no = self.list.GetSelectedItemCount()
        for j in range(no):
            i = self.list.GetFirstSelected()
            self.list.DeleteItem(i)

    def onAdd(self, event):
        if self.key == '':
            dlg = TwoItemList(self, title=self.title, key=self.key, label1=self.label1, label2=self.label2)
            dlg.ShowModal()
            if hasattr(dlg, 'result1') and hasattr(dlg, 'result2'):
                self.list.Append([dlg.result1, dlg.result2])
        else:
            dlg = ThreeItemList(self, title=self.title, key=self.key, label1=self.label1, label2=self.label2)
            dlg.ShowModal()
            if self.key == "Teacher":
                if hasattr(dlg, 'result1') and hasattr(dlg, 'result2') and hasattr(dlg, 'result3') and hasattr(dlg, 'result4') :
                    if dlg.result1 in globaldata.teacher_fullnames or dlg.result2 in globaldata.teacher_shortnames:
                        dl = wx.MessageDialog(None, 'Duplicate Entry: ' + dlg.result1 + ' ' + dlg.result2, "Error", wx.OK|wx.ICON_ERROR)
                        dl.ShowModal()
                        dl.Destroy()
                        return
                    self.list.Append([dlg.result1, dlg.result2, dlg.result3, dlg.result4])
            else:
                if hasattr(dlg, 'result1') and hasattr(dlg, 'result2') and hasattr(dlg, 'result3'):
                    if dlg.result1 in globaldata.venue_fullnames or dlg.result1 in globaldata.class_fullnames or dlg.result1 in globaldata.subject_fullnames or dlg.result2 in globaldata.venue_shortnames or dlg.result2 in globaldata.class_shortnames or dlg.result2 in globaldata.subject_shortnames:
                        dl = wx.MessageDialog(None, 'Duplicate Entry: ' + dlg.result1 + ' ' + dlg.result2, "Error", wx.OK|wx.ICON_ERROR)
                        dl.ShowModal()
                        dl.Destroy()
                        return
                    self.list.Append([dlg.result1, dlg.result2, dlg.result3])
        # dlg.Destroy()

    def onOK(self, event):
        self.result1 = []
        self.result2 = []
        self.result3 = []
        self.result4 = []

        n = self.list.GetItemCount()
        if self.key == "Teacher":
            for i in range(n):
                x = self.list.GetItem(i, 0)
                y = self.list.GetItem(i, 1)
                z = self.list.GetItem(i, 2)
                w = self.list.GetItem(i, 3)
                self.result1.append(x.GetText())
                self.result2.append(y.GetText())
                self.result3.append(int(z.GetText()))
                self.result4.append(int(w.GetText()))
        elif self.key == '':
            for i in range(n):
                x = self.list.GetItem(i, 0)
                y = self.list.GetItem(i, 1)
                self.result1.append(x.GetText())
                self.result2.append(y.GetText())
        else:
            for i in range(n):
                x = self.list.GetItem(i, 0)
                y = self.list.GetItem(i, 1)
                z = self.list.GetItem(i, 2)
                self.result1.append(x.GetText())
                self.result2.append(y.GetText())
                self.result3.append(int(z.GetText()))
        self.Destroy()

class TwoItemList(wx.Dialog):
    def __init__(self, parent, size=(600,50), id=-1, title="Enter Values",key='', label1='', label2=""):
        self.key = key
        wx.Dialog.__init__(self, parent, id, title, size=(800,80))
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.AddSpacer(10)

        self.label1 = wx.StaticText(self, label=label1)
        self.label2 = wx.StaticText(self, label=label2)

        if label1 == "Teacher":
            self.field1 = PromptingComboBox(self, "Choose", globaldata.teacher_shortnames,'Teacher', key='') 
        elif label1 == "Venue": 
            self.field1 = PromptingComboBox(self, "Choose", globaldata.venue_shortnames,'Venue', key='')
        if label2 == "Class / Batch":
            self.field2 = PromptingComboBox(self, "Choose", globaldata.class_shortnames,'Class', key='')
        elif label2 == "Subject":
            self.field2 = PromptingComboBox(self, "Choose", globaldata.subject_shortnames,'Subject', key='')


        self.mainSizer.Add(self.label1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)

        self.okbutton = wx.Button(self, label="OK")
        self.mainSizer.Add(self.okbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.canbutton = wx.Button(self, wx.ID_CANCEL, label='Cancel')
        self.mainSizer.Add(self.canbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.onClosed, self.canbutton)
        self.Bind(wx.EVT_BUTTON, self.onOK, self.okbutton)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        self.SetSizer(self.mainSizer)
        self.result = None
        # self.Bind(wx.EVT_CLOSE, self.onClosed)
        self.okbutton.SetFocus()

    def onClosed(self, event):
        print 'Close pressed'
        self.Destroy()

    def onOK(self, event):
        self.result1 = self.field1.res
        self.result2 = self.field2.res
        self.Destroy()

class ThreeItemList(wx.Dialog):
    def __init__(self, parent, size=(600,50), id=-1, title="Enter Values",key='', label1=' Name :', label2="Abbrevation:"):
        self.key = key
        wx.Dialog.__init__(self, parent, id, title, size=(850,80))
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.AddSpacer(10)

        self.label1 = wx.StaticText(self, label=key + label1)
        self.field1 = wx.TextCtrl(self, value="")
        self.label2 = wx.StaticText(self, label=label2)
        self.field2 = wx.TextCtrl(self, value="")                

        self.mainSizer.Add(self.label1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)

        if key == "Subject":
            self.label3 = wx.StaticText(self, label="NoOfHours:")
            self.field3 = wx.TextCtrl(self, value="")                
            self.mainSizer.Add(self.label3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
            self.mainSizer.Add(self.field3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
            self.mainSizer.AddSpacer(10)

        elif key == "Teacher":
            self.label3 = wx.StaticText(self, label="WeeklyMax Load:")
            self.field3 = wx.TextCtrl(self, value="")                
            self.label4 = wx.StaticText(self, label="DailyMax Load:")
            self.field4 = wx.TextCtrl(self, value="")                
            self.mainSizer.Add(self.label3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
            self.mainSizer.Add(self.field3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
            self.mainSizer.AddSpacer(10)
            self.mainSizer.Add(self.label4, 1, flag=wx.ALIGN_CENTER_VERTICAL)
            self.mainSizer.Add(self.field4, 1, flag=wx.ALIGN_CENTER_VERTICAL)
            self.mainSizer.AddSpacer(10)

        else:
            self.label3 = wx.StaticText(self, label="Capacity:")
            self.field3 = wx.TextCtrl(self, value="")                
            self.mainSizer.Add(self.label3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
            self.mainSizer.Add(self.field3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
            self.mainSizer.AddSpacer(10)

        self.okbutton = wx.Button(self, label="OK")
        self.mainSizer.Add(self.okbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.canbutton = wx.Button(self, wx.ID_CANCEL, label='Cancel')
        self.mainSizer.Add(self.canbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.onClosed, self.canbutton)
        self.Bind(wx.EVT_BUTTON, self.onOK, self.okbutton)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        self.SetSizer(self.mainSizer)
        self.result = None
        # self.Bind(wx.EVT_CLOSE, self.onClosed)
        self.okbutton.SetFocus()

    def onClosed(self, event):
        print 'Close pressed'
        self.result = None
        self.Destroy()

    def onOK(self, event):
        self.result1 = self.field1.GetValue()
        self.result2 = self.field2.GetValue()
        self.result3 = self.field3.GetValue()
        if self.key == "Teacher":
            self.result4 = self.field4.GetValue()
        self.Destroy()

    # def onCancel(self, event):
    #     self.result = None
    #     self.Destroy()


class PromptingComboBox(wx.ComboBox) :
    def __init__(self, parent, value, choices, name, style=0, key='NotTwo', **par):
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, value, style= wx.CB_DROPDOWN|wx.CB_SORT, choices=choices, **par)
        self.parent = parent
        self.choices = choices
        self.name = name
        self.key = key
        self.Bind(wx.EVT_COMBOBOX, self.EvtCombobox) 
        self.Bind(wx.EVT_TEXT_ENTER, self.TypedText) 
        # self.Bind(wx.EVT_TEXT, self.EvtText)
        # self.Bind(wx.EVT_CHAR, self.EvtChar)
        self.ignoreEvtText = False
                
    def TypedText(self, event):
        res = self.GetValue()
        if res in self.choices:
            self.EvtCombobox(event)
        else:
            self.SetValue("Choose")

    def EvtChar(self, event):
        if event.GetKeyCode() == 8:
            self.ignoreEvtText = True
        event.Skip()

    def EvtText(self, event):
        if self.ignoreEvtText:
            self.ignoreEvtText = False
            return
        currentText = event.GetString()
        found = False
        for choice in self.choices :
            if choice.startswith(currentText):
                self.ignoreEvtText = True
                self.SetValue(choice)
                self.SetInsertionPoint(len(currentText))
                self.SetMark(len(currentText), len(choice))
                found = True
                self.res = self.GetValue()
                break
        if not found:
            event.Skip()
            
    def EvtCombobox(self, event):
        self.ignoreEvtText = True
        # print globaldata.teacher_class_map
        # print 'selected', self.GetValue()
        self.res = self.GetValue()
        key = self.res
        if self.key == 'NotTwo':
            if self.res != "ADD NEW":
                if self.name == "Teacher":
                    #TeacherClass map
                    try:
                        val = globaldata.teacher_class_map[key]
                    except:
                        val = None
                    if val != None and self.parent.field3.GetValue() == "Choose":
                        self.parent.field3.SetValue(val)
                        self.parent.field3.res = val
                        #check if above line causes any bugs in other functions
                    #TeacherSubject map
                    try:
                        val = globaldata.teacher_subject_map[key]
                    except:
                        val = None
                    if val != None and self.parent.field4.GetValue() == "Choose":
                        self.parent.field4.SetValue(val)
                        self.parent.field4.res = val
                elif self.name == "Venue":
                    #VenueClass map
                    try:
                        val = globaldata.venue_class_map[key]
                    except:
                        val = None
                    if val != None and self.parent.field3.GetValue() == "Choose":
                        self.parent.field3.SetValue(val)
                        self.parent.field3.res = val

                elif self.name == "Class":

                    #ClassVenue map
                    try:
                        val = globaldata.class_venue_map[key]
                    except:
                        val = None
                    if val != None and self.parent.field2.GetValue() == "Choose":
                        self.parent.field2.SetValue(val)
                        self.parent.field2.res = val
                    #ClassTeacher map
                    try:
                        val = globaldata.class_teacher_map[key]
                    except:
                        val = None
                    if val != None and self.parent.field1.GetValue() == "Choose":
                        self.parent.field1.SetValue(val)
                        self.parent.field1.res = val

                    #ClassSubject map
                    try:
                        key = key.split('-')[0]
                        val = globaldata.class_subject_map[key]
                    except:
                        val = None
                    if val != None:
                        #make sub dropdown
                        self.parent.field4.Clear()
                        for sub in val:
                            self.parent.field4.Append(sub)
                    else:
                        self.parent.field4.Clear()
                        for sub in globaldata.subject_shortnames[1:]:
                            self.parent.field4.Append(sub)

                elif self.name == "Subject":
                    #SubjectTeacher map
                    try:
                        val = globaldata.subject_teacher_map[key]
                    except:
                        val = None
                    if val != None and self.parent.field1.GetValue() == "Choose":
                        self.parent.field1.SetValue(val)
                        self.parent.field1.res = val

                    #SubjectClass map
                    try:
                        val = globaldata.subject_class_map[key]
                    except:
                        val = None
                    if val != None and self.parent.field3.GetValue() == "Choose":
                        self.parent.field3.SetValue(val)
                        self.parent.field3.res = val

                    
                # del self.res
        if self.res == "ADD NEW" :
            if self.name == "Teacher":
                dlg = ThreeItemList(self, title="Enter Teacher Data", key="Teacher")
                dlg.ShowModal()
                if hasattr(dlg, 'result1') and hasattr(dlg, 'result2') and hasattr(dlg, 'result3') and hasattr(dlg, 'result4'):
                    globaldata.teacher_fullnames.append(dlg.result1)
                    globaldata.teacher_shortnames.append(dlg.result2)
                    globaldata.teacher_weeklymax.append(int(dlg.result3))
                    globaldata.teacher_dailymax.append(int(dlg.result4))
                    self.Append(dlg.result2)
                    self.parent.field1.SetValue(dlg.result2)
                    self.parent.field1.res = dlg.result2
                else:
                    self.SetValue('Choose')
                    del self.res
                dlg.Destroy()
            elif self.name == "Venue":
                dlg = ThreeItemList(self, title="Enter Venue Data", key="Venue")
                dlg.ShowModal()
                if hasattr(dlg, 'result1') and hasattr(dlg, 'result2') and hasattr(dlg, 'result3'):
                    globaldata.venue_fullnames.append(dlg.result1)
                    globaldata.venue_shortnames.append(dlg.result2)
                    globaldata.venue_capacity.append(int(dlg.result3))
                    self.Append(dlg.result2)
                    self.parent.field2.SetValue(dlg.result2)
                    self.parent.field2.res = dlg.result2
                else:
                    self.SetValue('Choose')
                    del self.res
                dlg.Destroy()        
            elif self.name == "Class":
                dlg = ThreeItemList(self, title="Enter Class Data", key="Class")
                dlg.ShowModal()
                if hasattr(dlg, 'result1') and hasattr(dlg, 'result2') and hasattr(dlg, 'result3'):
                    globaldata.class_fullnames.append(dlg.result1)
                    globaldata.class_shortnames.append(dlg.result2)
                    globaldata.class_capacity.append(int(dlg.result3))
                    self.Append(dlg.result2)
                    self.parent.field3.SetValue(dlg.result2)
                    self.parent.field3.res = dlg.result2
                else:
                    self.SetValue('Choose')
                    del self.res
                dlg.Destroy()
            elif self.name == "Subject":
                dlg = ThreeItemList(self, title="Enter Subject Data", key="Subject")
                dlg.ShowModal()
                if hasattr(dlg, 'result1') and hasattr(dlg, 'result2') and hasattr(dlg, 'result3'):
                    globaldata.subject_fullnames.append(dlg.result1)
                    globaldata.subject_shortnames.append(dlg.result2)
                    globaldata.subject_credits.append(int(dlg.result3))
                    globaldata.subjects[dlg.result2] = int(dlg.result3)
                    self.Append(dlg.result2)
                    self.parent.field4.SetValue(dlg.result2)
                    self.parent.field4.res = dlg.result2
                else:
                    self.SetValue('Choose')
                    del self.res
                dlg.Destroy()
        self.parent.okbutton.SetFocus()
        event.Skip()

class Dialoge(wx.Dialog):
    def __init__(self, parent, id=-1, title="Enter Values"):
        wx.Dialog.__init__(self, parent, id, title,size=(900,50))
        self.warn = True
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.AddSpacer(10)
        self.label1 = wx.StaticText(self, label="Teacher:")
        self.field1 = PromptingComboBox(self, "Choose", globaldata.teacher_shortnames,'Teacher') 
        # self.field1 = wx.TextCtrl(self, value="")
        self.label2 = wx.StaticText(self, label="Venue:")
        self.field2 = PromptingComboBox(self, "Choose", globaldata.venue_shortnames, 'Venue') 
        # self.field2 = wx.TextCtrl(self, value="")
        self.label3 = wx.StaticText(self, label="Class:")
        self.field3 = PromptingComboBox(self, "Choose", globaldata.class_shortnames, 'Class') 
        # self.field3 = wx.TextCtrl(self, value="")
        self.label4 = wx.StaticText(self, label="Subject:")
        self.field4 = PromptingComboBox(self, "Choose", globaldata.subject_shortnames, 'Subject') 
    
        self.okbutton = wx.Button(self, label="OK", id=wx.ID_OK)
        self.okbutton.SetFocus()

        self.canbutton = wx.Button(self, label="CANCEL", id=wx.ID_CANCEL)
    
        #got name of Teacher/Venue/Class
        self.name = parent.name
        if self.name in globaldata.all_teachers:
            self.field1.SetValue(self.name)
            self.field1.res = self.name
        elif self.name in globaldata.all_venues:
            self.field2.SetValue(self.name)
            self.field2.res = self.name
        elif self.name in globaldata.all_classes:
            self.field3.SetValue(self.name)
            self.field3.res = self.name
            key = self.name.split('-')[0]
            if key in globaldata.class_subject_map:
                val = globaldata.class_subject_map[key]
                self.field4.Clear()
                for sub in val:
                    self.field4.Append(sub)


        self.mainSizer.Add(self.label1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field1, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field2, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.label3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field3, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)


        self.mainSizer.Add(self.label4, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.Add(self.field4, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.canbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(5)
        self.mainSizer.Add(self.okbutton, 1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.mainSizer.AddSpacer(5)
        
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        self.Bind(wx.EVT_CLOSE, self.Closed, id=wx.ID_CANCEL)

        self.SetSizer(self.mainSizer)
        self.result = None
    
    def Closed(self, event):
        # print 'Close pressed'
        self.result = None
        self.Destroy()

    def onOK(self, event):
        if not hasattr(self.field1, 'res') or not hasattr(self.field2,"res") or not hasattr(self.field3, "res") or not hasattr(self.field4, "res"):
            print 'NO res'
            return

        # if self.field1.res == "ADD NEW" or self.field2.res == "ADD NEW" or self.field3.res == "ADD NEW" or self.field4.res == "ADD NEW":
        #     return

        if self.warn:
            venueIn = globaldata.venue_shortnames.index(self.field2.res) - 1
            venueCap = globaldata.venue_capacity[venueIn]

            classIn = globaldata.class_shortnames.index(self.field3.res) - 1
            classCap = globaldata.class_capacity[classIn]

            if venueCap < classCap:
                dlg = wx.MessageDialog(None, "Venue Capacity not sufficient for Class\nChange the venue or Click OK to continue anyway", "Notice", wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
                ret = dlg.ShowModal()
                dlg.Destroy()
                if ret == wx.ID_OK:
                    print  'OK'
                elif ret == wx.ID_CANCEL:
                    return

        self.result1 = self.field1.res
        self.result2 = self.field2.res
        self.result3 = self.field3.res
        self.result4 = self.field4.res
        
        self.Destroy()

    def onCancel(self, event):
        self.result = None
        self.Destroy()

class HeaderInfo(wx.Dialog):
    def __init__(self, parent, id=-1, title="Enter Values"):
        wx.Dialog.__init__(self, parent, id, title,size=(700,400))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.AddSpacer(10)
        self.heading_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)

        self.label1 = wx.StaticText(self, label="Enter Title For Timetable:")
        self.label1.SetFont(self.heading_font)
        self.label2 = wx.StaticText(self, label="(It will be displayed above the timetable)")

        self.h1 = wx.BoxSizer(wx.VERTICAL)
        self.h1.Add(self.label1, 1)
        self.h1.Add(self.label2, 1)
        self.mainSizer.Add(self.h1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.l1 = wx.StaticText(self, label="Title 1:")
        self.l2 = wx.StaticText(self, label="Title 2:")
        self.l3 = wx.StaticText(self, label="Title 3:")

        self.f1 = wx.TextCtrl(self, value="", size=(150,-1))
        self.f2 = wx.TextCtrl(self, value="", size=(150,-1))
        self.f3 = wx.TextCtrl(self, value="", size=(150,-1))

        self.h1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h1.Add(self.l1, 1)
        self.h1.Add(self.f1, 1)
        self.mainSizer.Add(self.h1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.h1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h1.Add(self.l2, 1)
        self.h1.Add(self.f2, 1)
        self.mainSizer.Add(self.h1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.h1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h1.Add(self.l3, 1)
        self.h1.Add(self.f3, 1)        
        self.mainSizer.Add(self.h1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(10)

        self.okbutton = wx.Button(self, label="OK", id=wx.ID_OK)
        self.okbutton.SetFocus()

        self.canbutton = wx.Button(self, label="Cancel", id=wx.ID_CANCEL)
        
        self.mainSizer.Add(self.okbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.canbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(10)
        
        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.onClosed, id=wx.ID_CANCEL)

        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        # self.Bind(wx.EVT_CLOSE, self.Closed)
        
        self.SetSizer(self.mainSizer)
        self.result = None


    def onClosed(self, event):
        print 'Close pressed'
        self.result = None
        self.Destroy()

    def onOK(self, event):
        self.result1 = self.f1.GetValue()
        self.result2 = self.f2.GetValue()
        self.result3 = self.f3.GetValue()
        self.Destroy()

    def onCancel(self, event):
        self.result = None
        self.Destroy()


class BasicConstraint(wx.Dialog):

    def __init__(self, parent, id=-1, title="Enter Values"):

        wx.Dialog.__init__(self, parent, id, title,size=(500,400))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainSizer.AddSpacer(10)        
        self.heading_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        
        self.label1 = wx.StaticText(self, label="Enter Basic Constraints:")
        self.label1.SetFont(self.heading_font)
        self.vv = wx.BoxSizer(wx.VERTICAL)
        self.vv.Add(self.label1, 1, wx.EXPAND)
        self.mainSizer.Add(self.vv, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)


        self.v1 = wx.BoxSizer(wx.HORIZONTAL)
        self.ldays = wx.StaticText(self, label="Working days per week")
        self.tdays = wx.TextCtrl(self, value="7")
        self.v1.Add(self.ldays, 1, wx.EXPAND|wx.ALIGN_CENTER)
        self.v1.AddSpacer(10)
        self.v1.Add(self.tdays, 1, wx.EXPAND)

        self.v2 = wx.BoxSizer(wx.HORIZONTAL)
        self.llectures = wx.StaticText(self, label="Lectures per day")
        self.tlectures = wx.TextCtrl(self, value="10")
        self.v2.Add(self.llectures, 1, wx.EXPAND)
        self.v2.Add(self.tlectures, 1, wx.EXPAND)

        self.h1 = wx.BoxSizer(wx.VERTICAL)
        self.h1.Add(self.v1, 1, wx.EXPAND)
        self.h1.AddSpacer(10)        
        self.h1.Add(self.v2, 1, wx.EXPAND)
        self.mainSizer.Add(self.h1, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)


        self.mainSizer.AddSpacer(50)

        self.label3 = wx.StaticText(self, label="Class:")
        self.label3.SetFont(self.heading_font)

        self.hh = wx.BoxSizer(wx.VERTICAL)
        self.hh.Add(self.label3, 1, flag=wx.EXPAND)
        self.mainSizer.Add(self.hh, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)


        self.h4 = wx.BoxSizer(wx.HORIZONTAL)
        self.lclassmax = wx.StaticText(self, label="Weekly Maximum Workload ")
        self.tclassmax = wx.TextCtrl(self, value="30",size=(140,-1))
        self.h4.Add(self.lclassmax, 1, flag=wx.ALIGN_CENTER|wx.EXPAND)
        self.h4.Add(self.tclassmax, 1, flag=wx.EXPAND)
 
        self.h5 = wx.BoxSizer(wx.HORIZONTAL)
        self.lclassmin = wx.StaticText(self, label="Lecture Start Time")
        self.tclassmin = wx.TextCtrl(self, value="15",size=(140,-1))
        self.h5.Add(self.lclassmin, 1, flag=wx.ALIGN_CENTER|wx.EXPAND)
        self.h5.Add(self.tclassmin, 1, flag=wx.EXPAND)

        self.vv = wx.BoxSizer(wx.VERTICAL)
        self.vv.Add(self.h4, 1, flag=wx.EXPAND)
        self.vv.AddSpacer(10)
        self.vv.Add(self.h5, 1, flag=wx.EXPAND)
        self.mainSizer.Add(self.vv, 1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(10)
                
        self.okbutton = wx.Button(self, label="OK", id=wx.ID_OK)
        self.okbutton.SetFocus()

        self.canbutton = wx.Button(self, label="Cancel", id=wx.ID_CANCEL)

        self.mainSizer.Add(self.okbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(10)
        self.mainSizer.Add(self.canbutton, 0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.mainSizer.AddSpacer(20)

        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        self.Bind(wx.EVT_BUTTON, self.onClosed, id=wx.ID_CANCEL)

        self.SetSizer(self.mainSizer)
        self.result = None

        # self.Bind(wx.EVT_CLOSE, self.Closed)

    def onClosed(self, event):
        print 'Close pressed'
        self.result = None
        self.Destroy()

    def onOK(self, event):
        self.days = self.tdays.GetValue()
        self.lectures = self.tlectures.GetValue()
        
        # self.daily_max = self.tdailymax.GetValue()
        # self.daily_min = self.tdailymin.GetValue()

        # self.weekly_max = self.tweeklymax.GetValue()
        # self.weekly_min = self.tweeklymin.GetValue()

        self.class_max = self.tclassmax.GetValue()
        self.start_time = self.tclassmin.GetValue()
        self.Destroy()

    # def onCancel(self, event):
    #     self.result = None
    #     self.Destroy()