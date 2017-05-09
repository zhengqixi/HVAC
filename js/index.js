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
      });
    });
  });
  
// endpoint: /standard/total_usage?start=12312&end=123123
//  var standard_total_usage = {
//    "3rd floor lighting and plugs": 99.89861111111115, 
//    "4th floor lighting and plugs": 189.71638888888893, 
//    "4th floor mechanical 2nd,3rd,5th lighting and plugs": 1341.8322222222223, 
//    "6th floor lighting and plugs": 446.0686111111111, 
//    "7th floor lighting and plugs": 461.3552777777777, 
//    "7th floor mechanical, 8th and 9th lighting and plugs": 1970.6208333333343, 
//    "Other-Utility1": 6666.403055555554, 
//    "Other-Utility2": 15526.48444444445, 
//    "Total": 15799.24666666667, 
//    "Utility 1": 11525.850000000002, 
//    "Utility 2": 4273.3966666666665, 
//    "cellar power and lighting": 1782.5644444444445, 
//    "elevator": 516.0638888888888, 
//    "retail": 400.8063888888889, 
//    "roof mechanical": 10141.851944444448, 
//    "sub-cellar power and lighting": 4842.108888888887
//  }
  
// endpoint: /standard/utility_comparison?start=123&end=213123
//  var standard_utility_comparison = {
//    "Utility 1": 11525.850000000002, 
//    "Utility 1 ranking": [
//      [
//        "retail", 
//        400.8063888888889
//      ], 
//      [
//        "6th floor lighting and plugs", 
//        446.0686111111111
//      ], 
//      [
//        "7th floor lighting and plugs", 
//        461.3552777777777
//      ], 
//      [
//        "elevator", 
//        516.0638888888888
//      ], 
//      [
//        "sub-cellar power and lighting", 
//        4842.108888888887
//      ]
//    ], 
//    "Utility 2": 4273.3966666666665, 
//    "Utility 2 ranking": [
//      [
//        "3rd floor lighting and plugs", 
//        99.89861111111115
//      ], 
//      [
//        "4th floor lighting and plugs", 
//        189.71638888888893
//      ], 
//      [
//        "4th floor mechanical 2nd,3rd,5th lighting and plugs", 
//        1341.8322222222223
//      ], 
//      [
//        "cellar power and lighting", 
//        1782.5644444444445
//      ], 
//      [
//        "7th floor mechanical, 8th and 9th lighting and plugs", 
//        1970.6208333333343
//      ], 
//      [
//        "roof mechanical", 
//        10141.851944444448
//      ]
//    ]
//  }
  
// endpoint: /standard/<board>?start=123&end=213123
//  var standard_board = {
//    "daily": [
//      275.37055555555554, 
//      125.43583333333333
//    ], 
//    "max": 275.37055555555554, 
//    "mean": 200.40319444444444, 
//    "min": 125.43583333333333, 
//    "time": [
//      1449014400000000000, 
//      1449100800000000000
//    ]
//  }
  
// endpoint: /night_day/total_usage?start=1448&end=1440&peak_start=9:00&peak_end=17:00
//  var night_day_total_usage = {
//    "off_peak": {
//      "3rd floor lighting and plugs": 0.3761111111111111, 
//      "4th floor lighting and plugs": 5.380833333333333, 
//      "4th floor mechanical 2nd,3rd,5th lighting and plugs": 573.5958333333333, 
//      "6th floor lighting and plugs": 58.598611111111104, 
//      "7th floor lighting and plugs": 6.677222222222222, 
//      "7th floor mechanical, 8th and 9th lighting and plugs": 541.495, 
//      "Other-Utility1": 2892.3838888888895, 
//      "Other-Utility2": 4509.727777777778, 
//      "Total": 3798.465, 
//      "Utility 1": 2721.0750000000003, 
//      "Utility 2": 1077.39, 
//      "cellar power and lighting": 702.7758333333336, 
//      "elevator": 105.63194444444444, 
//      "retail": 227.90638888888887, 
//      "roof mechanical": 2686.104166666667, 
//      "sub-cellar power and lighting": 2493.5697222222225
//    }, 
//    "on_peak": {
//      "3rd floor lighting and plugs": 34.72666666666666, 
//      "4th floor lighting and plugs": 65.02416666666667, 
//      "4th floor mechanical 2nd,3rd,5th lighting and plugs": 676.8763888888888, 
//      "6th floor lighting and plugs": 149.68583333333333, 
//      "7th floor lighting and plugs": 162.92972222222224, 
//      "7th floor mechanical, 8th and 9th lighting and plugs": 837.6250000000001, 
//      "Other-Utility1": 2374.978333333333, 
//      "Other-Utility2": 5823.7411111111105, 
//      "Total": 5924.373333333333, 
//      "Utility 1": 4007.1749999999993, 
//      "Utility 2": 1917.1983333333333, 
//      "cellar power and lighting": 742.8861111111112, 
//      "elevator": 221.51361111111112, 
//      "retail": 155.4125, 
//      "roof mechanical": 3466.6027777777776, 
//      "sub-cellar power and lighting": 1685.4366666666665
//    }
//  }
  
// endpoint: /night_day/utility_comparison?start=1448946000000&end=1449118800000&peak_start=9:00&peak_end=17:00
//  var night_day_utility_comparison = {
//    "off_peak": {
//      "Utility 1": 2721.0750000000003, 
//      "Utility 1 ranking": [
//        [
//          "7th floor lighting and plugs", 
//          6.677222222222222
//        ], 
//        [
//          "6th floor lighting and plugs", 
//          58.598611111111104
//        ], 
//        [
//          "elevator", 
//          105.63194444444444
//        ], 
//        [
//          "retail", 
//          227.90638888888887
//        ], 
//        [
//          "sub-cellar power and lighting", 
//          2493.5697222222225
//        ]
//      ], 
//      "Utility 2": 1077.39, 
//      "Utility 2 ranking": [
//        [
//          "3rd floor lighting and plugs", 
//          0.3761111111111111
//        ], 
//        [
//          "4th floor lighting and plugs", 
//          5.380833333333333
//        ], 
//        [
//          "7th floor mechanical, 8th and 9th lighting and plugs", 
//          541.495
//        ], 
//        [
//          "4th floor mechanical 2nd,3rd,5th lighting and plugs", 
//          573.5958333333333
//        ], 
//        [
//          "cellar power and lighting", 
//          702.7758333333336
//        ], 
//        [
//          "roof mechanical", 
//          2686.104166666667
//        ]
//      ]
//    }, 
//    "on_peak": {
//      "Utility 1": 4007.1749999999993, 
//      "Utility 1 ranking": [
//        [
//          "6th floor lighting and plugs", 
//          149.68583333333333
//        ], 
//        [
//          "retail", 
//          155.4125
//        ], 
//        [
//          "7th floor lighting and plugs", 
//          162.92972222222224
//        ], 
//        [
//          "elevator", 
//          221.51361111111112
//        ], 
//        [
//          "sub-cellar power and lighting", 
//          1685.4366666666665
//        ]
//      ], 
//      "Utility 2": 1917.1983333333333, 
//      "Utility 2 ranking": [
//        [
//          "3rd floor lighting and plugs", 
//          34.72666666666666
//        ], 
//        [
//          "4th floor lighting and plugs", 
//          65.02416666666667
//        ], 
//        [
//          "4th floor mechanical 2nd,3rd,5th lighting and plugs", 
//          676.8763888888888
//        ], 
//        [
//          "cellar power and lighting", 
//          742.8861111111112
//        ], 
//        [
//          "7th floor mechanical, 8th and 9th lighting and plugs", 
//          837.6250000000001
//        ], 
//        [
//          "roof mechanical", 
//          3466.6027777777776
//        ]
//      ]
//    }
//  }
  
// endpoint: /night_day/retail?start=14480&end=1449&peak_start=9:00&peak_end=17:00
//  var night_day_board = {
//    "off_peak": {
//      "daily": [
//        160.75388888888887, 
//        67.1525
//      ], 
//      "max": 160.75388888888887, 
//      "mean": 113.95319444444443, 
//      "min": 67.1525, 
//      "time": [
//        1449014400000000000, 
//        1449100800000000000
//      ]
//    }, 
//    "on_peak": {
//      "daily": [
//        107.58083333333335, 
//        47.831666666666656
//      ], 
//      "max": 107.58083333333335, 
//      "mean": 77.70625, 
//      "min": 47.831666666666656, 
//      "time": [
//        1449014400000000000, 
//        1449100800000000000
//      ]
//    }
//  }
  
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