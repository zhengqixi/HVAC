function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; }
  tablinks = document.getElementsByClassName("tab-link");
  for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

$(document).ready(function () {
  const $baseURL = 'http://energy.cooper.edu/analytics/engine/'
  
  $('#standard-query').click(function() {
    let start = new Date($('#standard-start').val()).getTime();
    let end = new Date($('#standard-end').val()).getTime();
    $.getJSON($baseURL + '/standard/total_usage?start=' + start + '&end=' + end, function(response) {
      createPieChart('standard-aggregate', 'Aggregate Power Usage', 'Distribution Board', formatTotalUsageData(response), 'left');
    });
    $.getJSON($baseURL + '/standard/utility_comparison?start=' + start + '&end=' + end, function(response) {
      createPieChart('standard-utility', 'Utility Comparison', 'Utility', formatUtilityComparison(response), 'center');
      formatUtilityRanking('#suc-', response);
    });
  });
  
  $('#daynight-query').click(function() {
    let start = new Date($('#daynight-start').val()).getTime();
    let end = new Date($('#daynight-end').val()).getTime();
    let peakSH = formatHour($('#daynight-sh').val());
    let peakSM = $('#daynight-sm').val();
    let peakEH = formatHour($('#daynight-eh').val());
    let peakEM = $('#daynight-em').val();
    $.getJSON($baseURL + '/night_day/total_usage?start=' + start + '&end=' + end + '&peak_start=' + peakSH + ":" + peakSM + "&peak_end=" + peakEH + ":" + peakEM, function(response) {
      $.each(response, function(k, v) {
        createPieChart('daynight-aggregate-' + k, 'Aggregate Power Usage (' + k + ')', 'Distribution Board', formatTotalUsageData(v), 'left');
      });
    });
    $.getJSON($baseURL + '/night_day/utility_comparison?start=' + start + '&end=' + end + '&peak_start=' + peakSH + ":" + peakSM + "&peak_end=" + peakEH + ":" + peakEM, function(response) {
      $.each(response, function(k, v) {
        createPieChart('daynight-utility-' + k, 'Utility Comparison (' + k + ')', 'Utility', formatUtilityComparison(v), 'center');
        formatUtilityRanking('#dnuc-', v);
      });
    });
  });
  
  function formatHour(h) {
    if (h.length < 2) {
      return "0" + h;
    } else {
      return h;
    }
  }
  
  function formatTotalUsageData(data) {
    return $.map(data, function(k,v){
      if (v != "Total" && v != "Utility 1" && v != "Utility 2") {
        return {name: v, y: k};
      };
    });
  }
  
  function formatUtilityComparison(data) {
    return $.map(data, function(k,v){
      if (typeof k == "number") {
        return {name: v, y: k};
      };
    });
  }
  
  function formatUtilityRanking(id, data) {
    var i = 0;
    $.each(data, function(k,v){
      if (typeof v == "object") {
        var str = "<h1>Utility " + (i + 1) + "</h1>"
        v.forEach(function(db) {
          str += db[0] + ": <b>" + db[1].toFixed(2) + " kW </b><br />";
        });
        $(id + i).html(str);
        i++;
      };
    });
  }
  
  function createPieChart(elementId, chartTitle, seriesName, data, legendAlign) {
    Highcharts.chart(elementId, {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
      },
      colors: [
        '#ed1c24','#00aeef','#ffcf06','#00914d','#363639'
      ],
      credits: {
        enabled: false
      },
      title: {
        text: chartTitle
      },
      tooltip: {
        pointFormat: 'Power Usage: <b>{point.y:.2f}kW</b><br/>Percentage: <b>{point.percentage:.1f}%</b>'
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
          enabled: false
        },
          showInLegend: true
        }
      },
      legend: {
        align: legendAlign
      },
      series: [{
        name: seriesName,
        colorByPoint: true,
        data: data
      }]
    });
  }
});