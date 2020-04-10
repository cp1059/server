

menu_top = [
    {
        "label": "首页",
        "path": "/dashboard",
        "icon": 'el-icon-s-home',
        "meta": {
            "i18n": 'dashboard',
        },
        "parentId": 0
    }
]

first = [
{
        "label": "公共",
        "path": '/publicinfo',
        "meta": {
            "i18n": 'publicinfo',
        },
        "icon": 'el-icon-setting',
        "children": [
            {
                "label": "轮播图",
                "path": 'banner',
                "component": 'views/custom/publicinfo/banner',
                "meta": {
                    "i18n": 'banner'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
            {
                "label": "视频",
                "path": 'video',
                "component": 'views/custom/publicinfo/video',
                "meta": {
                    "i18n": 'video'
                },
                "icon": 'el-icon-setting',
                "children": []
            }
        ]
    },
    {
        "label": "彩票",
        "path": '/cpinfo',
        "meta": {
            "i18n": 'cpinfo',
        },
        "icon": 'el-icon-setting',
        "children": [
            {
                "label": "彩票类型",
                "path": 'cpTypes',
                "meta": {
                    "i18n": 'cpTypes',
                },
                "icon": 'el-icon-setting',
                "children":[
                    {
                        "label": "彩票大类",
                        "path": 'cpbigtype',
                        "component": 'views/custom/cpinfo/cpTypes/cpbigtype',
                        "meta": {
                            "i18n": 'cpbigtype'
                        },
                        "icon": 'el-icon-setting',
                        "children": []
                    },
                    {
                        "label": "彩票中类",
                        "path": 'cpsmalltype',
                        "component": 'views/custom/cpinfo/cpTypes/cpsmalltype',
                        "meta": {
                            "i18n": 'cpsmalltype'
                        },
                        "icon": 'el-icon-setting',
                        "children": []
                    },
                    {
                        "label": "彩票小类",
                        "path": 'cpminitype',
                        "component": 'views/custom/cpinfo/cpTypes/cpminitype',
                        "meta": {
                            "i18n": 'cpminitype'
                        },
                        "icon": 'el-icon-setting',
                        "children": []
                    },
                    {
                        "label": "彩票玩法",
                        "path": 'cpgames',
                        "component": 'views/custom/cpinfo/cpTypes/cpgames',
                        "meta": {
                            "i18n": 'cpgames'
                        },
                        "icon": 'el-icon-setting',
                        "children": []
                    },
                ]
            },
            {
                "label": "彩票",
                "path": 'cp',
                "component": 'views/custom/cpinfo/cp',
                "meta": {
                    "i18n": 'cp'
                },
                "icon": 'el-icon-setting',
                "children": []
            }
        ]
    },
    {
        "label": "系统管理",
        "path": '/systemManagement',
        "meta": {
            "i18n": 'systemManagement',
        },
        "icon": 'el-icon-setting',
        "children": [
            {
                "label": "初始化项目",
                "path": 'InitProject',
                "component": 'views/custom/systeminfo/InitProject',
                "meta": {
                    "i18n": 'InitProject'
                },
                "icon": 'el-icon-setting',
                "children": []
            },
            {
                "label": "刷新缓存",
                "path": 'Cache',
                "component": 'views/custom/systeminfo/Cache',
                "meta": {
                    "i18n": 'Cache'
                },
                "icon": 'el-icon-setting',
                "children": []
            }
        ]
    }
]


all_menu = {
    "top" : menu_top,
    "first" : first
}
