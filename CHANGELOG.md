# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.1.1] - 2023-07-18

- Implement `openapi_extra: x-access-needed` [shared/backlog #164](https://gitlab.internal.verihubs.com/verihubs/product/shared/backlog/-/issues/164)

## [1.1.0] - 2023-06-12

### Changed

- Changed list notification to utilize cursor pagination [#12](https://gitlab.internal.verihubs.com/verihubs-engineering/cloud-services/utility/notification-service/-/issues/12)

### Fixed

- Fixed error exception handler on `422 Unprocessable Content`

## [1.0.0] - 2023-05-05

### Added

- Added `GET /v1/notification/account/{account_id}/notification` [Get account notifications] to fetch notification based on account_id [#5](https://gitlab.internal.verihubs.com/verihubs-engineering/cloud-services/utility/notification-service/-/issues/5)
- Initialize `notification subscriber` to `send email` to recipient via `email-service` and `create notification` based on given content [#5](https://gitlab.internal.verihubs.com/verihubs-engineering/cloud-services/utility/notification-service/-/issues/5)

[1.1.1]: https://gitlab.internal.verihubs.com/verihubs-engineering/cloud-services/utility/notification-service/-/compare/1.1.0...1.1.1
[1.1.0]: https://gitlab.internal.verihubs.com/verihubs-engineering/cloud-services/utility/notification-service/-/compare/1.0.0...1.1.0
[1.0.0]: https://gitlab.internal.verihubs.com/verihubs-engineering/cloud-services/utility/notification-service/-/tags/1.0.0