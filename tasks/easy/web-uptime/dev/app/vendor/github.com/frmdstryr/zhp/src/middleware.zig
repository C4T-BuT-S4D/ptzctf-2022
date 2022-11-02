// -------------------------------------------------------------------------- //
// Copyright (c) 2019-2020, Jairus Martin.                                    //
// Distributed under the terms of the MIT License.                            //
// The full license is in the file LICENSE, distributed with this software.   //
// -------------------------------------------------------------------------- //
const std = @import("std");
const web = @import("zhp.zig");
const log = std.log;
const Handler = web.Handler;
const Application = web.Application;
const ServerRequest = web.ServerRequest;

pub const LoggingMiddleware = struct {
    pub fn processResponse(_: *Application, server_request: *ServerRequest) !void {
        const request = &server_request.request;
        const response = &server_request.response;
        log.info("{d} {s} {s} ({s}) {d}", .{ response.status.code, @tagName(request.method), request.path, request.client, response.body.items.len });
    }
};

pub const RedirectMiddleware = struct {
    pub fn processRequest(app: *Application, server_request: *ServerRequest) !void {
        const request = &server_request.request;
        if (request.path.len < 1) {
            return;
        }

        const resolved = try std.fs.path.resolvePosix(app.allocator, &[_][]const u8{request.path});
        if (!std.mem.eql(u8, resolved, request.path)) {
            try server_request.response.redirect(resolved);
            try server_request.connection.sendResponse(server_request);
        }
    }

    pub fn processResponse(app: *Application, server_request: *ServerRequest) !void {
        const redirect = server_request.response.headers.get("Location") catch |err| switch (err) {
            error.KeyError => return,
            else => return err,
        };
        app.allocator.free(redirect);
    }
};

pub const SessionMiddleware = struct {
    // If you want storage use it statically

    pub fn processRequest(app: *Application, server_request: *ServerRequest) !void {
        _ = app;
        _ = server_request;
    }

    pub fn processResponse(app: *Application, server_request: *ServerRequest) !void {
        _ = app;
        _ = server_request;
    }
};
