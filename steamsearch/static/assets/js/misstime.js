/*
 * @Author: your name
 * @Date: 2020-09-26 23:03:33
 * @LastEditTime: 2020-09-27 10:49:27
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: /steamsearch/static/assets/js/birthday.js
 */
(function ($) {
    $.extend({
        ms_DatePicker1: function (options) {
            var defaults = {
                YearSelector1: "#sel_year1",
                MonthSelector1: "#sel_month1",
                DaySelector1: "#sel_day1",
                MinSelector1: "#sel_min1",
                HourSelector1: "#sel_hour1",
                // FirstText: "请选择",
                FirstValue: 0
            };
            var opts = $.extend({}, defaults, options);
            var $YearSelector1 = $(opts.YearSelector1);
            var $MonthSelector1 = $(opts.MonthSelector1);
            var $DaySelector1 = $(opts.DaySelector1);
            var $HourSelector1 = $(opts.HourSelector1);
            var $MinSelector1 = $(opts.MinSelector1);
            // var FirstText = opts.FirstText;
            // var FirstValue = opts.FirstValue;

            // 初始化
            var stry = "<option value=\"" + "none" + "\">" + "请选择年" + "</option>";
            var strm = "<option value=\"" + "none" + "\">" + "请选择月" + "</option>";
            var strd = "<option value=\"" + "none" + "\">" + "请选择日" + "</option>";
            var strh = "<option value=\"" + "none" + "\">" + "请选择小时" + "</option>";
            var strmin = "<option value=\"" + "none" + "\">" + "请选择分钟" + "</option>";

            $YearSelector1.html(stry);
            $MonthSelector1.html(strm);
            $DaySelector1.html(strd);
            $HourSelector1.html(strh);
            $MinSelector1.html(strmin);

            // 年份列表
            var yearNow = new Date().getFullYear();
            var yearSel = $YearSelector1.attr("rel");
            for (var i = yearNow; i >= 1900; i--) {
                var sed = yearSel == i ? "selected" : "";
                var yearStr = "<option value=\"" + i + "\" " + sed + ">" + i + "年</option>";
                $YearSelector1.append(yearStr);
            }

            // 月份列表
            var monthSel = $MonthSelector1.attr("rel");
            for (var i = 1; i <= 12; i++) {
                var sed = monthSel == i ? "selected" : "";
                var monthStr = "<option value=\"" + i + "\" " + sed + ">" + i + "月</option>";
                $MonthSelector1.append(monthStr);
            }
            // 小时份列表
            var HourSel = $HourSelector1.attr("rel");
            for (var i = 1; i <= 24; i++) {
                var sed = HourSel == i ? "selected" : "";
                var hourStr = "<option value=\"" + i + "\" " + sed + ">" + i + "点</option>";
                $HourSelector1.append(hourStr);
            }
            //分钟列表
            var MinSel = $MinSelector1.attr("rel");
            for (var i = 1; i <= 60; i++) {
                var sed = MinSel == i ? "selected" : "";
                var minStr = "<option value=\"" + i + "\" " + sed + ">" + i + "分</option>";
                $MinSelector1.append(minStr);
            }
            // 日列表(仅当选择了年月)
            function BuildDay() {
                if ($YearSelector1.val() == 0 || $MonthSelector1.val() == 0) {
                    // 未选择年份或者月份
                    $DaySelector1.html(strd);
                } else {
                    $DaySelector1.html(strd);
                    var year = parseInt($YearSelector1.val());
                    var month = parseInt($MonthSelector1.val());
                    var dayCount = 0;
                    switch (month) {
                        case 1:
                        case 3:
                        case 5:
                        case 7:
                        case 8:
                        case 10:
                        case 12:
                            dayCount = 31;
                            break;
                        case 4:
                        case 6:
                        case 9:
                        case 11:
                            dayCount = 30;
                            break;
                        case 2:
                            dayCount = 28;
                            if ((year % 4 == 0) && (year % 100 != 0) || (year % 400 == 0)) {
                                dayCount = 29;
                            }
                            break;
                        default:
                            break;
                    }

                    var daySel = $DaySelector1.attr("rel");
                    for (var i = 1; i <= dayCount; i++) {
                        var sed = daySel == i ? "selected" : "";
                        var dayStr = "<option value=\"" + i + "\" " + sed + ">" + i + "日</option>";
                        $DaySelector1.append(dayStr);
                    }
                }
            }
            $MonthSelector1.change(function () {
                BuildDay();
            });
            $MinSelector1.change(function () {
                BuildDay();
            });
            $HourSelector1.change(function () {
                BuildDay();
            });
            $YearSelector1.change(function () {
                BuildDay();
            });
            if ($DaySelector1.attr("rel") != "") {
                BuildDay();
            }
        } // End ms_DatePicker
    });
})(jQuery);