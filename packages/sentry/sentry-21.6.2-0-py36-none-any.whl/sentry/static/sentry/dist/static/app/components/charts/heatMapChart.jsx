import { __assign, __extends, __rest } from "tslib";
import './components/visualMap';
import * as React from 'react';
import HeatMapSeries from './series/heatMapSeries';
import BaseChart from './baseChart';
var HeatMapChart = /** @class */ (function (_super) {
    __extends(HeatMapChart, _super);
    function HeatMapChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    HeatMapChart.prototype.render = function () {
        var _a = this.props, series = _a.series, seriesOptions = _a.seriesOptions, visualMaps = _a.visualMaps, props = __rest(_a, ["series", "seriesOptions", "visualMaps"]);
        return (<BaseChart options={{
                visualMap: visualMaps,
            }} {...props} series={series.map(function (_a) {
                var seriesName = _a.seriesName, data = _a.data, dataArray = _a.dataArray, options = __rest(_a, ["seriesName", "data", "dataArray"]);
                return HeatMapSeries(__assign(__assign(__assign({}, seriesOptions), options), { name: seriesName, data: dataArray || data.map(function (_a) {
                        var value = _a.value, name = _a.name;
                        return [name, value];
                    }) }));
            })}/>);
    };
    return HeatMapChart;
}(React.Component));
export default HeatMapChart;
//# sourceMappingURL=heatMapChart.jsx.map