import React from 'react';
import { withTheme } from '@emotion/react';
import SegmentExplorerQuery from 'app/utils/performance/segmentExplorer/segmentExplorerQuery';
import TagKeyHistogramQuery from 'app/utils/performance/segmentExplorer/tagKeyHistogramQuery';
import { SpanOperationBreakdownFilter } from '../filter';
import { getTransactionField } from '../tagExplorer';
import TagsHeatMap from './tagsHeatMap';
import { TagValueTable } from './tagValueTable';
var TAG_VALUE_LIMIT = 10;
var HISTOGRAM_BUCKET_LIMIT = 20;
var TagsDisplay = function (props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, projects = props.projects, tagKey = props.tagKey;
    var aggregateColumn = getTransactionField(SpanOperationBreakdownFilter.None, projects, eventView);
    if (!tagKey) {
        return null;
    }
    return (<React.Fragment>
      <TagKeyHistogramQuery eventView={eventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} limit={HISTOGRAM_BUCKET_LIMIT} tagKey={tagKey} sort="-frequency">
        {function (_a) {
            var isLoading = _a.isLoading, tableData = _a.tableData;
            return <TagsHeatMap {...props} tableData={tableData} isLoading={isLoading}/>;
        }}
      </TagKeyHistogramQuery>
      <SegmentExplorerQuery eventView={eventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} tagKey={tagKey} limit={TAG_VALUE_LIMIT} sort="-frequency" allTagKeys>
        {function (_a) {
            var isLoading = _a.isLoading, tableData = _a.tableData;
            return <TagValueTable {...props} tableData={tableData} isLoading={isLoading}/>;
        }}
      </SegmentExplorerQuery>
    </React.Fragment>);
};
export default withTheme(TagsDisplay);
//# sourceMappingURL=tagsDisplay.jsx.map