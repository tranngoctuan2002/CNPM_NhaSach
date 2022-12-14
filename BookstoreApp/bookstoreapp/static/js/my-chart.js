function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function drawCateStats(labels, data) {
 const ctx = document.getElementById('cateStats');
 const randomNum = () => Math.floor(Math.random() * (235 - 52 + 1) + 52);
 const randomRGB = () => 'rgb(${randomNum()}, ${randomNum()}, ${randomNum()})';

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: "Doanh thu",
        data: data,
        borderWidth: 1,
        backgroundColor: getRandomColor
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins: {
    legend: {
      display: false
    }
  },
      title: {
        display: true,
        text: 'Biểu đồ Doanh thu từng tháng theo các loại sách'
      }
    }
  });
}

function drawRevenueStats(labels, data) {
const ctx = document.getElementById('revenueStats');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Doanh Thu',
        data: data,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
