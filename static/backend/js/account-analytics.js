'use strict';

(function () {
    let cardColor, labelColor, headingColor, borderColor, legendColor;
    const data = document.currentScript.dataset
    const visitors_by_os = JSON.parse(data.visitors_by_os ? data.visitors_by_os.replaceAll("'", '"') : "[]")
    const visitors_by_browser = JSON.parse(data.visitors_by_browser ? data.visitors_by_browser.replaceAll("'", '"') : "[]")
    const visitors_by_device = JSON.parse(data.visitors_by_device ? data.visitors_by_device.replaceAll("'", '"') : "[]")
    const visitors_by_country = JSON.parse(data.visitors_by_country ? data.visitors_by_country.replaceAll("'", '"') : "[]")
    const countries = JSON.parse(data.countries ? data.countries.replaceAll("'", '"') : "[]")

    // Color constant
    const chartColors = {
        column: {
            series1: '#826af9',
            series2: '#d2b0ff',
            bg: '#f8d3ff'
        },
        donut: {
            series1: '#fdd835',
            series2: '#32baff',
            series3: '#ffa1a1',
            series4: '#7367f0',
            series5: '#29dac7'
        },
        area: {
            series1: '#ab7efd',
            series2: '#b992fe',
            series3: '#e0cffe'
        }
    };

    if (isDarkStyle) {
        cardColor = config.colors_dark.cardColor;
        labelColor = config.colors_dark.textMuted;
        headingColor = config.colors_dark.headingColor;
        legendColor = config.colors_dark.bodyColor;
        borderColor = config.colors_dark.borderColor;
    } else {
        cardColor = config.colors.cardColor;
        labelColor = config.colors.textMuted;
        headingColor = config.colors.headingColor;
        legendColor = config.colors.bodyColor;
        borderColor = config.colors.borderColor;
    }

    // Sessions line chart
    // --------------------------------------------------------------------
    const sessionsChartEl = document.querySelector('#sessions'),
        sessionsChartConfig = {
            chart: {
                height: 102,
                type: 'line',
                parentHeightOffset: 0,
                toolbar: {
                    show: false
                }
            },
            grid: {
                borderColor: labelColor,
                strokeDashArray: 6,
                xaxis: {
                    lines: {
                        show: true
                    }
                },
                yaxis: {
                    lines: {
                        show: false
                    }
                },
                padding: {
                    top: -15,
                    left: -7,
                    right: 7,
                    bottom: -15
                }
            },
            colors: [config.colors.info],
            stroke: {
                width: 3
            },
            series: [
                {
                    data: [0, 20, 5, 30, 15, 45]
                }
            ],
            xaxis: {
                labels: {
                    show: false
                },
                axisTicks: {
                    show: false
                },
                axisBorder: {
                    show: false
                }
            },
            yaxis: {
                labels: {
                    show: false
                }
            },
            tooltip: {
                enabled: false,
                shared: false,
                intersect: true,
                x: {
                    show: false
                }
            },
            markers: {
                size: 6,
                strokeWidth: 3,
                strokeColors: 'transparent',
                colors: ['transparent'],
                discrete: [
                    {
                        seriesIndex: 0,
                        dataPointIndex: 5,
                        fillColor: cardColor,
                        strokeColor: config.colors.info,
                        size: 6,
                        shape: 'circle'
                    }
                ],
                hover: {
                    size: 7
                }
            },
            responsive: [
                {
                    breakpoint: 1441,
                    options: {
                        chart: {
                            height: 70
                        }
                    }
                },
                {
                    breakpoint: 1310,
                    options: {
                        chart: {
                            height: 90
                        }
                    }
                },
                {
                    breakpoint: 1189,
                    options: {
                        chart: {
                            height: 70
                        }
                    }
                },
                {
                    breakpoint: 1025,
                    options: {
                        chart: {
                            height: 73
                        }
                    }
                },
                {
                    breakpoint: 992,
                    options: {
                        chart: {
                            height: 102
                        }
                    }
                }
            ]
        };
    if (typeof sessionsChartEl !== undefined && sessionsChartEl !== null) {
        const sessionsChart = new ApexCharts(sessionsChartEl, sessionsChartConfig);
        sessionsChart.render();
    }

    // Total Transactions Bar Chart
    // --------------------------------------------------------------------
    const totalTransactionChartEl = document.querySelector('#totalTransactionChart'),
        totalTransactionChartConfig = {
            chart: {
                height: 218,
                stacked: true,
                type: 'bar',
                parentHeightOffset: 0,
                toolbar: {
                    show: false
                }
            },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return Math.abs(val);
                    }
                }
            },
            legend: {show: false},
            dataLabels: {enabled: false},
            colors: [config.colors.primary, config.colors.success],
            grid: {
                borderColor,
                xaxis: {lines: {show: true}},
                yaxis: {lines: {show: false}},
                padding: {
                    top: -5,
                    bottom: -25
                }
            },
            states: {
                hover: {filter: {type: 'none'}},
                active: {filter: {type: 'none'}}
            },
            plotOptions: {
                bar: {
                    borderRadius: 5,
                    barHeight: '30%',
                    horizontal: true,
                    endingShape: 'flat',
                    startingShape: 'rounded'
                }
            },
            xaxis: {
                position: 'top',
                axisTicks: {show: false},
                axisBorder: {show: false},
                categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                labels: {
                    formatter: function (val) {
                        return Math.abs(Math.round(val));
                    },
                    style: {
                        colors: labelColor,
                        fontFamily: 'Inter'
                    }
                }
            },
            yaxis: {labels: {show: false}},
            series: [
                {
                    name: 'Last Week',
                    data: [83, 153, 213, 279, 213, 153, 83]
                },
                {
                    name: 'This Week',
                    data: [-84, -156, -216, -282, -216, -156, -84]
                }
            ]
        };
    if (typeof totalTransactionChartEl !== undefined && totalTransactionChartEl !== null) {
        const totalTransactionChart = new ApexCharts(totalTransactionChartEl, totalTransactionChartConfig);
        totalTransactionChart.render();
    }

    // Performance Radar Chart
    // --------------------------------------------------------------------
    const performanceChartEl = document.querySelector('#performanceChart'),
        performanceChartConfig = {
            chart: {
                height: 247,
                type: 'radar',
                toolbar: {
                    show: false
                }
            },
            legend: {
                show: true,
                markers: {offsetX: -2},
                itemMargin: {horizontal: 10},
                fontFamily: 'Inter',
                fontSize: '15px',
                labels: {
                    colors: labelColor,
                    useSeriesColors: false
                }
            },
            plotOptions: {
                radar: {
                    polygons: {
                        strokeColors: borderColor,
                        connectorColors: borderColor
                    }
                }
            },
            yaxis: {
                show: false
            },
            series: [
                {
                    name: 'Income',
                    data: [70, 90, 80, 95, 75, 90]
                },
                {
                    name: 'Net Worth',
                    data: [110, 72, 62, 65, 100, 75]
                }
            ],
            colors: [config.colors.warning, config.colors.primary],
            xaxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                labels: {
                    show: true,
                    style: {
                        colors: [labelColor, labelColor, labelColor, labelColor, labelColor, labelColor],
                        fontSize: '15px',
                        fontFamily: 'Inter'
                    }
                }
            },
            fill: {
                opacity: [1, 0.9]
            },
            stroke: {
                show: false,
                width: 0
            },
            markers: {
                size: 0
            },
            grid: {
                show: false,
                padding: {
                    top: 0,
                    bottom: -10
                }
            },
            responsive: [
                {
                    breakpoint: 1398,
                    options: {
                        chart: {
                            height: 287
                        }
                    }
                },
                {
                    breakpoint: 1200,
                    options: {
                        chart: {
                            height: 393
                        }
                    }
                }
            ]
        };
    if (typeof performanceChartEl !== undefined && performanceChartEl !== null) {
        const performanceChart = new ApexCharts(performanceChartEl, performanceChartConfig);
        performanceChart.render();
    }

    // Total Revenue
    // --------------------------------------------------------------------
    const totalRevenueEl = document.querySelector('#totalRevenue'),
        totalRevenueConfig = {
            chart: {
                height: 115,
                type: 'bar',
                distributed: true,
                parentHeightOffset: 0,
                toolbar: {
                    show: false
                }
            },
            grid: {
                padding: {
                    top: -20,
                    left: -14,
                    right: 0,
                    bottom: -15
                },
                yaxis: {
                    lines: {show: false}
                }
            },
            series: [
                {
                    name: 'Earning',
                    data: [120, 200, 150, 120]
                },
                {
                    name: 'Expense',
                    data: [72, 120, 50, 65]
                }
            ],
            legend: {
                show: false
            },
            tooltip: {
                enabled: false
            },
            dataLabels: {
                enabled: false
            },
            colors: [config.colors.primary, config.colors.warning],
            plotOptions: {
                bar: {
                    borderRadius: 6,
                    columnWidth: '48%',
                    startingShape: 'rounded'
                }
            },
            states: {
                hover: {
                    filter: {
                        // type: 'none'
                    }
                },
                active: {
                    filter: {
                        type: 'none'
                    }
                }
            },
            xaxis: {
                labels: {
                    show: false
                },
                axisTicks: {
                    show: false
                },
                axisBorder: {
                    show: false
                }
            },
            yaxis: {
                labels: {
                    show: false
                }
            },
            responsive: [
                {
                    breakpoint: 834,
                    options: {
                        plotOptions: {
                            bar: {
                                borderRadius: 4
                            }
                        }
                    }
                },
                {
                    breakpoint: 768,
                    options: {
                        plotOptions: {
                            bar: {
                                borderRadius: 8
                            }
                        }
                    }
                },
                {
                    breakpoint: 426,
                    options: {
                        plotOptions: {
                            bar: {
                                borderRadius: 10
                            }
                        }
                    }
                }
            ]
        };
    if (typeof totalRevenueEl !== undefined && totalRevenueEl !== null) {
        const totalRevenue = new ApexCharts(totalRevenueEl, totalRevenueConfig);
        totalRevenue.render();
    }

    // Overview Chart
    // --------------------------------------------------------------------
    const overviewChartEl = document.querySelector('#overviewChart'),
        overviewChartConfig = {
            chart: {
                height: 134,
                type: 'radialBar',
                sparkline: {
                    enabled: true
                }
            },
            plotOptions: {
                radialBar: {
                    hollow: {
                        size: '55%'
                    },
                    dataLabels: {
                        name: {
                            show: false
                        },
                        value: {
                            show: true,
                            offsetY: 5,
                            fontWeight: 600,
                            fontSize: '1rem',
                            fontFamily: 'Inter',
                            color: headingColor
                        }
                    },
                    track: {
                        background: config.colors_label.secondary
                    }
                }
            },
            states: {
                hover: {
                    filter: {
                        type: 'none'
                    }
                },
                active: {
                    filter: {
                        type: 'none'
                    }
                }
            },
            stroke: {
                lineCap: 'round'
            },
            colors: [config.colors.primary],
            grid: {
                padding: {
                    bottom: -15
                }
            },
            series: [64],
            labels: ['Progress']
        };
    if (typeof overviewChartEl !== undefined && overviewChartEl !== null) {
        const overviewChart = new ApexCharts(overviewChartEl, overviewChartConfig);
        overviewChart.render();
    }

    // Sales Country Bar Chart
    // --------------------------------------------------------------------
    const salesCountryChartEl = document.querySelector('#salesCountryChart'),
        salesCountryChartConfig = {
            chart: {
                type: 'bar',
                height: 368,
                parentHeightOffset: 0,
                toolbar: {
                    show: false
                }
            },
            series: [
                {
                    name: 'Visits',
                    data: visitors_by_country
                }
            ],
            plotOptions: {
                bar: {
                    borderRadius: 10,
                    barHeight: '60%',
                    horizontal: true,
                    distributed: true,
                    startingShape: 'rounded',
                    dataLabels: {
                        position: 'bottom'
                    }
                }
            },
            dataLabels: {
                enabled: true,
                textAnchor: 'start',
                offsetY: 8,
                offsetX: 11,
                style: {
                    fontWeight: 600,
                    fontSize: '0.9375rem',
                    fontFamily: 'Inter'
                }
            },
            tooltip: {
                enabled: false
            },
            legend: {
                show: false
            },
            colors: [
                config.colors.primary,
                config.colors.success,
                config.colors.warning,
                config.colors.info,
                config.colors.danger
            ],
            grid: {
                strokeDashArray: 8,
                borderColor,
                xaxis: {lines: {show: true}},
                yaxis: {lines: {show: false}},
                padding: {
                    top: -18,
                    left: 21,
                    right: 33,
                    bottom: 10
                }
            },
            xaxis: {
                categories: countries,
                labels: {
                    formatter: function (val) {
                        return val
                    },
                    style: {
                        fontSize: '0.9375rem',
                        colors: labelColor,
                        fontFamily: 'Inter'
                    }
                },
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false
                }
            },
            yaxis: {
                labels: {
                    style: {
                        fontWeight: 600,
                        fontSize: '0.9375rem',
                        colors: headingColor,
                        fontFamily: 'Inter'
                    }
                }
            },
            states: {
                hover: {
                    filter: {
                        type: 'none'
                    }
                },
                active: {
                    filter: {
                        type: 'none'
                    }
                }
            }
        };
    if (typeof salesCountryChartEl !== undefined && salesCountryChartEl !== null) {
        const salesCountryChart = new ApexCharts(salesCountryChartEl, salesCountryChartConfig);
        salesCountryChart.render();
    }
    window.onload = function () {
    // Visitor BY OS Donut Chart
    // --------------------------------------------------------------------
    const visitorByBrowserDonutChartEl = document.querySelector('#visitorByOS'),
        visitorByBrowserDonutChartConfig = {
            chart: {
                height: 368,
                fontFamily: 'Inter',
                type: 'donut',
                events: {
                    dataPointMouseEnter: function (event, chartContext, config) {
                        var dataLabel = chartContext.w.globals.labels[config.dataPointIndex];
                        var dataValue = chartContext.w.globals.series[0][config.dataPointIndex];
                    }
                }
            },
            labels: visitors_by_os.map((item) => item.os_id),
            series: visitors_by_os.map((item) => item.count),
            colors: [
                chartColors.donut.series1,
                chartColors.donut.series3,
                chartColors.donut.series4,
                chartColors.donut.series5
            ],
            stroke: {
                show: false,
                curve: 'straight'
            },
            dataLabels: {
                enabled: true,
                formatter: function (val, opt) {
                    return `${opt.w.globals.labels[opt.seriesIndex]}: ${visitors_by_os[opt.seriesIndex].count}`
                }
            },
            legend: {
                show: true,
                position: 'bottom',
                markers: {offsetX: -3},
                itemMargin: {
                    vertical: 3,
                    horizontal: 10
                },
                labels: {
                    colors: legendColor,
                    useSeriesColors: false
                }
            },
            responsive: [
                {
                    breakpoint: 992,
                    options: {
                        chart: {
                            height: 380
                        },
                        legend: {
                            position: 'bottom',
                            labels: {
                                colors: legendColor,
                                useSeriesColors: false
                            }
                        }
                    }
                },
                {
                    breakpoint: 576,
                    options: {
                        chart: {
                            height: 320
                        },
                        plotOptions: {
                            pie: {
                                donut: {
                                    labels: {
                                        show: true,
                                        name: {
                                            fontSize: '1.5rem'
                                        },
                                        value: {
                                            fontSize: '1rem'
                                        },
                                        total: {
                                            fontSize: '1.5rem'
                                        }
                                    }
                                }
                            }
                        },
                        legend: {
                            position: 'bottom',
                            labels: {
                                colors: legendColor,
                                useSeriesColors: false
                            }
                        }
                    }
                },
                {
                    breakpoint: 420,
                    options: {
                        chart: {
                            height: 350
                        },
                        legend: {
                            show: false
                        }
                    }
                },
                {
                    breakpoint: 360,
                    options: {
                        chart: {
                            height: 250
                        },
                        legend: {
                            show: false
                        }
                    }
                }
            ]
        };
    if (typeof visitorByBrowserDonutChartEl !== undefined && visitorByBrowserDonutChartEl !== null) {
        const visitorByBrowserDonutChart = new ApexCharts(visitorByBrowserDonutChartEl, visitorByBrowserDonutChartConfig);
        visitorByBrowserDonutChart.render();
    }

    // Visitor BY Browser Donut Chart
    // --------------------------------------------------------------------
    const visitorByOSDonutChartEl = document.querySelector('#visitorByBrowser'),
        visitorByOSDonutChartConfig = {
            chart: {
                height: 368,
                fontFamily: 'Inter',
                type: 'donut',
                events: {
                    dataPointMouseEnter: function (event, chartContext, config) {
                        var dataLabel = chartContext.w.globals.labels[config.dataPointIndex];
                        var dataValue = chartContext.w.globals.series[0][config.dataPointIndex];
                    }
                }
            },
            labels: visitors_by_browser.map((item) => item.browser_id.split(' ').slice(0, 1).join(' ')),
            series: visitors_by_browser.map((item) => item.count),
            colors: [
                chartColors.donut.series1,
                chartColors.donut.series3,
                chartColors.donut.series4,
                chartColors.donut.series5
            ],
            stroke: {
                show: false,
                curve: 'straight'
            },
            dataLabels: {
                enabled: true,
                formatter: function (val, opt) {
                    return `${opt.w.globals.labels[opt.seriesIndex]}: ${visitors_by_browser[opt.seriesIndex].count}`
                }
            },
            legend: {
                show: true,
                position: 'bottom',
                markers: {offsetX: -3},
                itemMargin: {
                    vertical: 3,
                    horizontal: 10
                },
                labels: {
                    colors: legendColor,
                    useSeriesColors: false
                }
            },
            responsive: [
                {
                    breakpoint: 992,
                    options: {
                        chart: {
                            height: 380
                        },
                        legend: {
                            position: 'bottom',
                            labels: {
                                colors: legendColor,
                                useSeriesColors: false
                            }
                        }
                    }
                },
                {
                    breakpoint: 576,
                    options: {
                        chart: {
                            height: 320
                        },
                        plotOptions: {
                            pie: {
                                donut: {
                                    labels: {
                                        show: true,
                                        name: {
                                            fontSize: '1.5rem'
                                        },
                                        value: {
                                            fontSize: '1rem'
                                        },
                                        total: {
                                            fontSize: '1.5rem'
                                        }
                                    }
                                }
                            }
                        },
                        legend: {
                            position: 'bottom',
                            labels: {
                                colors: legendColor,
                                useSeriesColors: false
                            }
                        }
                    }
                },
                {
                    breakpoint: 420,
                    options: {
                        chart: {
                            height: 280
                        },
                        legend: {
                            show: false
                        }
                    }
                },
                {
                    breakpoint: 360,
                    options: {
                        chart: {
                            height: 250
                        },
                        legend: {
                            show: false
                        }
                    }
                }
            ]
        };
    if (typeof visitorByOSDonutChartEl !== undefined && visitorByOSDonutChartEl !== null) {
        const visitorByOSDonutChart = new ApexCharts(visitorByOSDonutChartEl, visitorByOSDonutChartConfig);
        visitorByOSDonutChart.render();
    }

    // Visitor BY Device Donut Chart
    // --------------------------------------------------------------------
    const visitorByDeviceDonutChartEl = document.querySelector('#visitorByDevice'),
        visitorByDeviceDonutChartConfig = {
            chart: {
                height: 368,
                fontFamily: 'Inter',
                type: 'donut',
                events: {
                    dataPointMouseEnter: function (event, chartContext, config) {
                        var dataLabel = chartContext.w.globals.labels[config.dataPointIndex];
                        var dataValue = chartContext.w.globals.series[0][config.dataPointIndex];
                    }
                }
            },
            labels: visitors_by_device.map((item) => item.device_id),
            series: visitors_by_device.map((item) => item.count),
            colors: [
                chartColors.donut.series1,
                chartColors.donut.series3,
                chartColors.donut.series4,
                chartColors.donut.series5
            ],
            stroke: {
                show: false,
                curve: 'straight'
            },
            dataLabels: {
                enabled: true,
                formatter: function (val, opt) {
                    return `${opt.w.globals.labels[opt.seriesIndex]}: ${visitors_by_device[opt.seriesIndex].count}`
                }
            },
            legend: {
                show: true,
                position: 'bottom',
                markers: {offsetX: -3},
                itemMargin: {
                    vertical: 3,
                    horizontal: 10
                },
                labels: {
                    colors: legendColor,
                    useSeriesColors: false
                }
            },
            responsive: [
                {
                    breakpoint: 992,
                    options: {
                        chart: {
                            height: 380
                        },
                        legend: {
                            position: 'bottom',
                            labels: {
                                colors: legendColor,
                                useSeriesColors: false
                            }
                        }
                    }
                },
                {
                    breakpoint: 576,
                    options: {
                        chart: {
                            height: 320
                        },
                        plotOptions: {
                            pie: {
                                donut: {
                                    labels: {
                                        show: true,
                                        name: {
                                            fontSize: '1.5rem'
                                        },
                                        value: {
                                            fontSize: '1rem'
                                        },
                                        total: {
                                            fontSize: '1.5rem'
                                        }
                                    }
                                }
                            }
                        },
                        legend: {
                            position: 'bottom',
                            labels: {
                                colors: legendColor,
                                useSeriesColors: false
                            }
                        }
                    }
                },
                {
                    breakpoint: 420,
                    options: {
                        chart: {
                            height: 280
                        },
                        legend: {
                            show: false
                        }
                    }
                },
                {
                    breakpoint: 360,
                    options: {
                        chart: {
                            height: 250
                        },
                        legend: {
                            show: false
                        }
                    }
                }
            ]
        };
    if (typeof visitorByDeviceDonutChartEl !== undefined && visitorByDeviceDonutChartEl !== null) {
        const visitorByDeviceDonutChart = new ApexCharts(visitorByDeviceDonutChartEl, visitorByDeviceDonutChartConfig);
        visitorByDeviceDonutChart.render();
    }
    };
    // Bar Chart
    // --------------------------------------------------------------------
    const barChart = document.getElementById('latestVisitorBarChart');
    if (barChart) {
        const barChartVar = new Chart(barChart, {
            type: 'bar',
            data: {
                labels: [
                    '7/12',
                    '8/12',
                    '9/12',
                    '10/12',
                    '11/12',
                    '12/12',
                    '13/12',
                    '14/12',
                    '15/12',
                    '16/12',
                    '17/12',
                    '18/12',
                    '19/12'
                ],
                datasets: [
                    {
                        data: [275, 90, 190, 205, 125, 85, 55, 87, 127, 150, 230, 280, 190],
                        backgroundColor: orangeLightColor,
                        borderColor: 'transparent',
                        maxBarThickness: 15,
                        borderRadius: {
                            topRight: 15,
                            topLeft: 15
                        }
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 500
                },
                plugins: {
                    tooltip: {
                        rtl: isRtl,
                        backgroundColor: cardColor,
                        titleColor: headingColor,
                        bodyColor: legendColor,
                        borderWidth: 1,
                        borderColor: borderColor
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: borderColor,
                            drawBorder: false,
                            borderColor: borderColor
                        },
                        ticks: {
                            color: labelColor
                        }
                    },
                    y: {
                        min: 0,
                        max: 400,
                        grid: {
                            color: borderColor,
                            drawBorder: false,
                            borderColor: borderColor
                        },
                        ticks: {
                            stepSize: 100,
                            color: labelColor
                        }
                    }
                }
            }
        });
    }
})();
