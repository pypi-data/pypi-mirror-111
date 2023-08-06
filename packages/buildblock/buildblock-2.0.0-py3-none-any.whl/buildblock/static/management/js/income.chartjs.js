!function(c){
    var r = function(){
        this.$body = c("body"),this.charts=[]
    };

    r.prototype.respChart = function(a, t, e, o) {
        var l = Chart.controllers.bar.prototype.draw;
        Chart.controllers.bar = Chart.controllers.bar.extend({
            draw:function(){
                l.apply(this,arguments);
                var r=this.chart.chart.ctx,a=r.fill;
                r.fill=function(){
                    r.save(),
                    r.shadowColor="rgba(0,0,0,0.01)",
                    r.shadowBlur=20,
                    r.shadowOffsetX=4,
                    r.shadowOffsetY=5,
                    a.apply(this,arguments),
                    r.restore()
                }
            }
        }),
        Chart.defaults.global.defaultFontColor = "#8391a2",
        Chart.defaults.scale.gridLines.color = "#8391a2";
        var i = a.get(0).getContext("2d"), d = c(a).parent();

        return new Chart(i, {type:"bar", data:e, options:o});
    },

    r.prototype.initCharts = function(){
        var r = [];

        if(0<c("#income-chart").length){
            var a = document.getElementById("income-chart").getContext("2d").createLinearGradient(0,500,0,150);
            a.addColorStop(0,"#fa5c7c"),a.addColorStop(1,"#727cf5");
            var t = {
                labels:chartLabels,
                datasets:[{
                    label: mainDataLabel,
                    backgroundColor:a,
                    borderColor:a,
                    hoverBackgroundColor:a,
                    hoverBorderColor:a,
                    data: chartDataset
                }]
            };

            r.push(this.respChart(c("#income-chart"),"Bar",t,{
                maintainAspectRatio:!1,
                legend:{display:!1},
                scales:{
                    yAxes:[{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: mainDataLabel
                        },
                        gridLines:{
                            display:!1,
                            color:"rgba(0,0,0,0.05)"
                        },
                        stacked:!1,
                        ticks:{
                            stepSize:chartStep,
                            beginAtZero: true
                        }
                    }],
                    xAxes:[{
                        barPercentage:.7,
                        categoryPercentage:.5,
                        stacked:!1,
                        gridLines:{color:"rgba(0,0,0,0.01)"}
                    }]
                }
            }))
        }

        return r
    },

    r.prototype.init = function(){
        var a = this;
        Chart.defaults.global.defaultFontFamily = '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif',
        a.charts = this.initCharts(),c(window).on("resize", function(r){
            c.each(a.charts,function(r,a){
                try{a.destroy()}catch(r){}
            }),
            a.charts=a.initCharts()
        })
    },
    c.ChartJs = new r,
    c.ChartJs.Constructor = r
}

(window.jQuery),function(r){
    window.jQuery.ChartJs.init()
}();
