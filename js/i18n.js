const i18nData = {
    en: {
        dashboard: "Dashboard",
        qrList: "QR List",
        qrManagement: "QR Management",
        backToList: "Back to List",
        edit: "Edit",
        cancelEdit: "Cancel Edit",
        save: "Save",
        basicInfo: "Basic Information",
        title: "Title",
        qrNumber: "QR Number",
        qrStatus: "QR Status",
        failureCode: "Failure Code",
        scope: "Scope",
        triggerArea: "Trigger Area",
        triggerDate: "Trigger Date",
        owner: "Owner",
        problemSeverity: "Problem Severity",
        target: "Target",
        closeDate: "Close Date",
        presentCannel: "Present Cannel",
        qrDetail: "QR Detail",
        noMatch: "No entries found matching criteria.",
        phenomenon: "Problem Phenomenon",
        measuresResult: "Measures & Result",
        action: "Action",
        result: "Result",
        goodLead: "Good Lead",
        evidence: "Evidence",
        conclusion: "Conclusion",
        nextStep: "Next Step",
        nextStepExecutor: "Next Step Executor",
        timeline: "Timeline (Logs)",
        uploadHint: "Click or Drag & Drop image here to upload",
        noPicture: "No picture uploaded.",
        addCase: "Add New QR Case",
        search: "Search",
        searchPlaceholder: "Search Title, Phenomenon, Action...",
        allStatus: "All Status",
        allAreas: "All Areas",
        allScopes: "All Scopes",
        allOwners: "All Owners",
        ongoing: "Ongoing",
        completed: "Completed",
        failed: "Failed",
        submit: "Submit",
        cancel: "Cancel",
        prev: "Previous",
        next: "Next",
        showing: "Showing",
        to: "to",
        of: "of",
        entries: "entries",
        caseTriggered: "QR Case Triggered"
    },
    zh: {
        dashboard: "仪表盘",
        qrList: "QR 列表",
        qrManagement: "QR 管理系统",
        backToList: "返回列表",
        edit: "编辑",
        cancelEdit: "取消编辑",
        save: "保存",
        basicInfo: "基本信息",
        title: "标题",
        qrNumber: "QR 编号",
        qrStatus: "状态",
        failureCode: "失效代码",
        scope: "范围",
        triggerArea: "触发区域",
        triggerDate: "触发日期",
        owner: "负责人",
        problemSeverity: "严重程度",
        target: "目标",
        closeDate: "关闭日期",
        presentCannel: "渠道",
        qrDetail: "QR 详情",
        noMatch: "没有匹配的记录。",
        phenomenon: "问题现象",
        measuresResult: "措施与结果",
        action: "措施",
        result: "结果",
        goodLead: "好经验",
        evidence: "证据",
        conclusion: "结论",
        nextStep: "下一步计划",
        nextStepExecutor: "执行人",
        timeline: "时间线 (日志)",
        uploadHint: "点击或拖拽图片到此处上传",
        noPicture: "未上传图片",
        addCase: "新增 QR 案例",
        search: "搜索",
        searchPlaceholder: "搜索标题、现象、措施...",
        allStatus: "所有状态",
        allAreas: "所有区域",
        allScopes: "所有范围",
        allOwners: "所有负责人",
        ongoing: "进行中",
        completed: "已完成",
        failed: "已失败",
        submit: "提交",
        cancel: "取消",
        prev: "上一页",
        next: "下一页",
        showing: "显示",
        to: "至",
        of: "共",
        entries: "条记录",
        caseTriggered: "QR 案例触发"
    }
};

function getI18nMixin() {
    return {
        setup() {
            const currentLang = Vue.ref(localStorage.getItem('qr_lang') || 'en');
            
            const t = (key) => {
                return i18nData[currentLang.value][key] || key;
            };

            const toggleLang = () => {
                currentLang.value = currentLang.value === 'en' ? 'zh' : 'en';
                localStorage.setItem('qr_lang', currentLang.value);
            };

            return { currentLang, t, toggleLang };
        }
    };
}
