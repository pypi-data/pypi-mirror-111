import { __makeTemplateObject } from "tslib";
import { withTheme } from '@emotion/react';
import styled from '@emotion/styled';
import HeatMapChart from 'app/components/charts/heatMapChart';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { Panel } from 'app/components/panels';
import QuestionTooltip from 'app/components/questionTooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { axisDuration, axisLabelFormatter } from 'app/utils/discover/charts';
var findRowKey = function (row) {
    return Object.keys(row).find(function (key) { return key.includes('histogram'); });
};
var TagsHeatMap = function (props) {
    var tableData = props.tableData, isLoading = props.isLoading;
    if (!tableData || !tableData.data || !tableData.data.length) {
        return null;
    }
    // TODO(k-fish): Replace with actual theme colors.
    var purples = ['#D1BAFC', '#9282F3', '#6056BA', '#313087', '#021156'];
    var rowKey = findRowKey(tableData.data[0]);
    if (!rowKey) {
        return null;
    }
    var columnNames = new Set();
    var xValues = new Set();
    var maxCount = 0;
    var _data = tableData.data.map(function (row) {
        var x = axisDuration(row[rowKey]);
        var y = row.tags_value;
        columnNames.add(y);
        xValues.add(x);
        maxCount = Math.max(maxCount, row.count);
        return [x, y, row.count];
    });
    _data.sort(function (a, b) {
        if (a[0] === b[0]) {
            return b[1] - a[1];
        }
        return b[0] - a[0];
    });
    // TODO(k-fish): Cleanup options
    var chartOptions = {
        height: 290,
        animation: false,
        colors: purples,
        tooltip: {},
        yAxis: {
            type: 'category',
            data: Array.from(columnNames),
            splitArea: {
                show: true,
            },
        },
        xAxis: {
            boundaryGap: true,
            type: 'category',
            splitArea: {
                show: true,
            },
            data: Array.from(xValues),
            axisLabel: {
                show: true,
                showMinLabel: true,
                showMaxLabel: true,
                formatter: function (value) { return axisLabelFormatter(value, 'Count'); },
            },
            axisLine: {},
            axisPointer: {
                show: false,
            },
            axisTick: {
                show: true,
                interval: 0,
                alignWithLabel: true,
            },
        },
        grid: {
            left: space(3),
            right: space(3),
            top: '25px',
            bottom: space(4),
        },
    };
    var visualMaps = [
        {
            min: 0,
            max: maxCount,
            show: false,
            orient: 'horizontal',
            calculable: true,
            inRange: {
                color: purples,
            },
        },
    ];
    var series = [];
    series.push({
        seriesName: 'Count',
        dataArray: _data,
        label: {
            show: true,
        },
        emphasis: {
            itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
        },
    }); // TODO(k-fish): Fix heatmap data typing
    var reloading = isLoading;
    var loading = isLoading;
    return (<StyledPanel>
      <StyledHeaderTitleLegend>
        {t('Heat Map')}
        <QuestionTooltip size="sm" position="top" title={t('This heatmap shows the frequency for each duration across the most common tag values')}/>
      </StyledHeaderTitleLegend>

      <TransitionChart loading={loading} reloading={reloading}>
        <TransparentLoadingMask visible={reloading}/>

        <HeatMapChart visualMaps={visualMaps} series={series} {...chartOptions}/>
      </TransitionChart>
    </StyledPanel>);
};
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  margin-bottom: 0;\n  border-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom-right-radius: 0;\n"], ["\n  padding: ", ";\n  margin-bottom: 0;\n  border-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom-right-radius: 0;\n"])), space(3));
var StyledHeaderTitleLegend = styled(HeaderTitleLegend)(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
export default withTheme(TagsHeatMap);
var templateObject_1, templateObject_2;
//# sourceMappingURL=tagsHeatMap.jsx.map