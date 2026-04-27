<template>
    <Pie :data="chartData" :options="chartOptions" />
</template>

<script>
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

export default {
    components: { Pie },
    props: {
        chartData: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            chartOptions: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Reservation Status'
                    }
                },
            }
        }
    }
}
</script>