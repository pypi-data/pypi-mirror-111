    var chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(231,233,237)'
    };
    var color = Chart.helpers.color;

    function readJson() {
        var json = $.ajax({
            url: "{{ url_for('static', filename='settings/settings.json') }}",
            dataType: 'json',
            async: false
        }).responseText;
            return JSON.parse(json);
    }

    let graph = readJson();

    let json_data;
    function get_data(){
        $.ajax({
            url: "/chart-data",
            method: "POST",
        })
        .done(function(data){
            json_data = JSON.parse(data.ResultSet);
            $('#len').html(json_data);
        });
        return json_data;
    };

    var stats = get_data();
    function update() {
        stats = get_data();
        console.log(stats);
    }
    setInterval(update, 1000);
    var canvas = document.getElementById("temperature");
    //canvas.style.backgroundColor = "rgba(255, 255, 255, 1)";
    canvas.style.backgroundColor = "#282f2f";
    var ctx = canvas.getContext('2d');
    ctx.canvas.height = 100;
    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: "CPU temperature",
                    data: [],
                    borderColor: color(chartColors.red).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.red,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                xAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "Current time",
                            fontSize: 16,
                            fontColor: "white"
                        },
                        ticks: {
                            fontSize: 18,
                            fontColor: "white"
                        },
                        type: 'realtime',
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        }
                    }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "Temperature  [℃]",
                            fontSize: 20,
                            fontColor: "white",
                        },
                        ticks: {
                            min: {{ session["graph"].chart.temperature.yaxes.min }},
                            max: {{ session["graph"].chart.temperature.yaxes.max }},
                            fontSize: 18,
                            stepSize: {{ session["graph"].chart.temperature.yaxes.step }},
                            fontColor: "white",
                            showLabelBackdrop: false
                        },
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        },
                        pointLabels: {
                            fontColor: 'white'
                        }
                    }
                ],
            },
            layout: {
                padding: {
                    left: 10,
                    right: 10,
                    top: 10,
                    bottom: 10
                }
            },
            legend: {
                position: 'top',
                labels: {
                    fontColor: 'white',
                    fontSize: 18,
                },
            },
            plugins: {
                streaming: {
                    duration: {{ session["graph"].chart.temperature.streaming.duration }},
                    refresh: 1000,
                    delay: 1000,
                    frameRate: 30,
                    pause: false,
                    onRefresh: function(chart) {
                        chart.data.datasets[0].data.push({
                            x: Date.now(),
                            y: stats.temperature
                        });
                    }
                },
            }
        }
    });

  Chart.plugins.register({
    beforeDraw: function(chartInstance) {
      var ctx = chartInstance.chart.ctx;
      ctx.fillStyle = "rgba(50, 50, 50, 1)";
      ctx.fillStyle = "#282f2f";
      ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
    }
  })

    var canvas2 = document.getElementById("usage");
    var ctx2 = canvas2.getContext('2d');
    ctx2.canvas.height = 100;
    var chart2 = new Chart(ctx2, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: "CPU1",
                    data: [],
                    borderColor: color(chartColors.red).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.red,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
                {
                    label: "CPU2",
                    data: [],
                    borderColor: color(chartColors.blue).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.blue,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
                {
                    label: "CPU3",
                    data: [],
                    borderColor: color(chartColors.yellow).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.yellow,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
                {
                    label: "CPU4",
                    data: [],
                    borderColor: color(chartColors.green).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.green,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
            ]
        },
        options: {
            scales: {
                xAxes: [
                    {
                        scaleLabel: {
                            display: false,
                            labelString: "Current time",
                            fontSize: 16,
                            fontColor: "white"
                        },
                        ticks: {
                            fontSize: 18,
                            fontColor: "white"
                        },
                        type: 'realtime',
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        }
                    }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "Usage [%]",
                            fontSize: 20,
                            fontColor: "white"
                        },
                        ticks: {
                            min: {{ session["graph"].chart.usage.yaxes.min }},
                            max: {{ session["graph"].chart.usage.yaxes.max }},
                            stepSize: {{ session["graph"].chart.usage.yaxes.step }},
                            fontSize: 18,
                            fontColor: "white",
                            showLabelBackdrop: false
                        },
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        },
                        pointLabels: {
                            fontColor: 'white'
                        }
                    }
                ],
            },
            layout: {
                padding: {
                    left: 10,
                    right: 10,
                    top: 10,
                    bottom: 10
                }
            },
            legend: {
                position: 'top',
                labels: {
                    fontColor: 'white',
                    fontSize: 18,
                },
            },
            plugins: {
                streaming: {
                    duration: {{ session["graph"].chart.usage.streaming.duration }},
                    refresh: 1000,
                    delay: 1000,
                    frameRate: 30,
                    pause: false,
                    onRefresh: function(chart2) {
                        chart2.data.datasets[0].data.push({
                            x: Date.now(),
                            y: stats.usage_cpu1
                        });
                        chart2.data.datasets[1].data.push({
                            x: Date.now(),
                            y: stats.usage_cpu2
                        });
                        chart2.data.datasets[2].data.push({
                            x: Date.now(),
                            y: stats.usage_cpu3
                        });
                        chart2.data.datasets[3].data.push({
                            x: Date.now(),
                            y: stats.usage_cpu4
                        });
                    }
                }
            }
        }
    });

    var canvas3 = document.getElementById("memory");
    var ctx3 = canvas3.getContext('2d');
    ctx3.canvas.height = 100;
    var chart3 = new Chart(ctx3, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: "CPU memory",
                    data: [],
                    borderColor: color(chartColors.red).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.red,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
                {
                    label: "GPU memory",
                    data: [],
                    borderColor: color(chartColors.blue).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.blue,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
            ]
        },
        options: {
            scales: {
                xAxes: [
                    {
                        scaleLabel: {
                            display: false,
                            labelString: "Current time",
                            fontSize: 16,
                            fontColor: "white"
                        },
                        ticks: {
                            fontSize: 18,
                            fontColor: "white"
                        },
                        type: 'realtime',
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        }
                    }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "Memory [MB]",
                            fontSize: 20,
                            fontColor: "white"
                        },
                        ticks: {
                            min: {{ session["graph"].chart.memory.yaxes.min }},
                            max: {{ session["graph"].chart.memory.yaxes.max }},
                            stepSize: {{ session["graph"].chart.memory.yaxes.step }},
                            fontSize: 18,
                            fontColor: "white",
                            showLabelBackdrop: false
                        },
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        },
                        pointLabels: {
                            fontColor: 'white'
                        }
                    }
                ],
            },
            layout: {
                padding: {
                    left: 10,
                    right: 10,
                    top: 10,
                    bottom: 10
                }
            },
            legend: {
                position: 'top',
                labels: {
                    fontColor: 'white',
                    fontSize: 18,
                },
            },
            plugins: {
                streaming: {
                    duration: {{ session["graph"].chart.memory.streaming.duration }},
                    refresh: 1000,
                    delay: 1000,
                    frameRate: 30,
                    pause: false,
                    onRefresh: function(chart3) {
                        chart3.data.datasets[0].data.push({
                            x: Date.now(),
                            y: stats.memory_cpu
                        });
                        chart3.data.datasets[1].data.push({
                            x: Date.now(),
                            y: stats.memory_gpu
                        });
                    }
                }
            }
        }
    });

    var canvas4 = document.getElementById("frequency");
    var ctx4 = canvas4.getContext('2d');
    ctx4.canvas.height = 100;
    var chart4 = new Chart(ctx4, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: "CPU frequency",
                    data: [],
                    borderColor: color(chartColors.red).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.red,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
                {
                    label: "Core frequency",
                    data: [],
                    borderColor: color(chartColors.blue).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.blue,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
            ]
        },
        options: {
            scales: {
                xAxes: [
                    {
                        scaleLabel: {
                            display: false,
                            labelString: "Current time",
                            fontSize: 16,
                            fontColor: "white"
                        },
                        ticks: {
                            fontSize: 18,
                            fontColor: "white"
                        },
                        type: 'realtime',
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        }
                    }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "Frequency [MHz]",
                            fontSize: 20,
                            fontColor: "white"
                        },
                        ticks: {
                            min: {{ session["graph"].chart.frequency.yaxes.min }},
                            max: {{ session["graph"].chart.frequency.yaxes.max }},
                            stepSize: {{ session["graph"].chart.frequency.yaxes.step }},
                            fontSize: 18,
                            fontColor: "white",
                            showLabelBackdrop: false
                        },
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        },
                        pointLabels: {
                            fontColor: 'white'
                        }
                    }
                ],
            },
            layout: {
                padding: {
                    left: 10,
                    right: 10,
                    top: 10,
                    bottom: 10
                }
            },
            legend: {
                position: 'top',
                labels: {
                    fontColor: 'white',
                    fontSize: 18,
                },
            },
            plugins: {
                streaming: {
                    duration: {{ session["graph"].chart.frequency.streaming.duration }},
                    refresh: 1000,
                    delay: 1000,
                    frameRate: 30,
                    pause: false,
                    onRefresh: function(chart4) {
                        chart4.data.datasets[0].data.push({
                            x: Date.now(),
                            y: stats.frequency_cpu
                        });
                        chart4.data.datasets[1].data.push({
                            x: Date.now(),
                            y: stats.frequency_core
                        });
                    }
                }
            }
        }
    });

    var canvas5 = document.getElementById("loadavg");
    var ctx5 = canvas5.getContext('2d');
    ctx5.canvas.height = 100;
    var chart5 = new Chart(ctx5, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: "1 min",
                    data: [],
                    borderColor: color(chartColors.red).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.red,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
                {
                    label: "5 min",
                    data: [],
                    borderColor: color(chartColors.blue).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.blue,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                },
                {
                    label: "15 min",
                    data: [],
                    borderColor: color(chartColors.yellow).alpha(0.8).rgbString(),
                    backgroundColor: chartColors.yellow,
                    pointBackgroundColor: "white",
                    pointBorderColor: "white",
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                xAxes: [
                    {
                        scaleLabel: {
                            display: false,
                            labelString: "Current time",
                            fontSize: 16,
                            fontColor: "white"
                        },
                        ticks: {
                            fontSize: 18,
                            fontColor: "white"
                        },
                        type: 'realtime',
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        }
                    }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: "Load average",
                            fontSize: 20,
                            fontColor: "white"
                        },
                        ticks: {
                            min: {{ session["graph"].chart.loadavg.yaxes.min }},
                            max: {{ session["graph"].chart.loadavg.yaxes.max }},
                            stepSize: {{ session["graph"].chart.loadavg.yaxes.step }},
                            fontSize: 18,
                            fontColor: "white",
                            showLabelBackdrop: false
                        },
                        gridLines: {
                            color: "rgba(255, 255, 255, 0.5)",
                            lineWidth: 0.75
                        },
                        pointLabels: {
                            fontColor: 'white'
                        }
                    }
                ],
            },
            layout: {
                padding: {
                    left: 10,
                    right: 10,
                    top: 10,
                    bottom: 10
                }
            },
            legend: {
                position: 'top',
                labels: {
                    fontColor: 'white',
                    fontSize: 18,
                },
            },
            plugins: {
                streaming: {
                    duration: {{ session["graph"].chart.loadavg.streaming.duration }},
                    refresh: 1000,
                    delay: 1000,
                    frameRate: 30,
                    pause: false,
                    onRefresh: function(chart5) {
                        chart5.data.datasets[0].data.push({
                            x: Date.now(),
                            y: stats.loadavg_1
                        });
                        chart5.data.datasets[1].data.push({
                            x: Date.now(),
                            y: stats.loadavg_5
                        });
                        chart5.data.datasets[2].data.push({
                            x: Date.now(),
                            y: stats.loadavg_15
                        });
                    }
                }
            }
        }
    });