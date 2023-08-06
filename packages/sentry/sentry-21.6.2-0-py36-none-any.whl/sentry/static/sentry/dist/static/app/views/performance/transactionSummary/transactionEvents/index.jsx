import { __assign, __extends, __read, __spreadArray } from "tslib";
import { Component } from 'react';
import { browserHistory } from 'react-router';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import EventView from 'app/utils/discover/eventView';
import { isAggregateField, SPAN_OP_BREAKDOWN_FIELDS, SPAN_OP_RELATIVE_BREAKDOWN_FIELD, } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { getTransactionName } from '../../utils';
import EventsPageContent from './content';
var TransactionEvents = /** @class */ (function (_super) {
    __extends(TransactionEvents, _super);
    function TransactionEvents() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generateEventsEventView(_this.props.location, getTransactionName(_this.props.location)),
        };
        _this.renderNoAccess = function () {
            return <Alert type="warning">{t("You don't have access to this feature")}</Alert>;
        };
        return _this;
    }
    TransactionEvents.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generateEventsEventView(nextProps.location, getTransactionName(nextProps.location)) });
    };
    TransactionEvents.prototype.getDocumentTitle = function () {
        var name = getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), t('Events')].join(' \u2014 ');
        }
        return [t('Summary'), t('Events')].join(' \u2014 ');
    };
    TransactionEvents.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projects = _a.projects, location = _a.location;
        var eventView = this.state.eventView;
        var transactionName = getTransactionName(location);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: __assign({}, location.query),
            });
            return null;
        }
        var shouldForceProject = eventView.project.length === 1;
        var forceProject = shouldForceProject
            ? projects.find(function (p) { return parseInt(p.id, 10) === eventView.project[0]; })
            : undefined;
        var projectSlugs = eventView.project
            .map(function (projectId) { return projects.find(function (p) { return parseInt(p.id, 10) === projectId; }); })
            .filter(function (p) { return p !== undefined; })
            .map(function (p) { return p.slug; });
        return (<SentryDocumentTitle title={this.getDocumentTitle()} orgSlug={organization.slug} projectSlug={forceProject === null || forceProject === void 0 ? void 0 : forceProject.slug}>
        <Feature features={['performance-events-page']} organization={organization} renderDisabled={this.renderNoAccess}>
          <GlobalSelectionHeader lockedMessageSubject={t('transaction')} shouldForceProject={shouldForceProject} forceProject={forceProject} specificProjectSlugs={projectSlugs} disableMultipleProjectSelection showProjectSettingsLink>
            <LightWeightNoProjectMessage organization={organization}>
              <EventsPageContent location={location} eventView={eventView} transactionName={transactionName} organization={organization} projects={projects}/>
            </LightWeightNoProjectMessage>
          </GlobalSelectionHeader>
        </Feature>
      </SentryDocumentTitle>);
    };
    return TransactionEvents;
}(Component));
function generateEventsEventView(location, transactionName) {
    if (transactionName === undefined) {
        return undefined;
    }
    // Use the user supplied query but overwrite any transaction or event type
    // conditions they applied.
    var query = decodeScalar(location.query.query, '');
    var conditions = tokenizeSearch(query);
    conditions
        .setTagValues('event.type', ['transaction'])
        .setTagValues('transaction', [transactionName]);
    Object.keys(conditions.tagValues).forEach(function (field) {
        if (isAggregateField(field))
            conditions.removeTag(field);
    });
    // Default fields for relative span view
    var fields = [
        'id',
        'user.display',
        SPAN_OP_RELATIVE_BREAKDOWN_FIELD,
        'transaction.duration',
        'trace',
        'timestamp',
        'spans.total.time',
    ];
    fields.push.apply(fields, __spreadArray([], __read(SPAN_OP_BREAKDOWN_FIELDS)));
    return EventView.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: fields,
        query: conditions.formatString(),
        projects: [],
        orderby: decodeScalar(location.query.sort, '-timestamp'),
    }, location);
}
export default withGlobalSelection(withProjects(withOrganization(TransactionEvents)));
//# sourceMappingURL=index.jsx.map