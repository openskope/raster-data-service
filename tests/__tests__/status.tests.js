const rest = require('rest');
const mime = require('rest/interceptor/mime');

const timeseriesServiceBase = 'http://localhost:8001/timeseries-service/api/v1';

const callRESTService =  rest.wrap(mime, { mime: 'application/json' } );

describe("When timeseries service is running ", () => {
    
    it ('GET /status should return service name', async function() {
        var response = await callRESTService({
            method: 'GET',
            path: timeseriesServiceBase + '/status'
        });
        expect(response.status.code).toBe(200);
        expect(response.entity.name).toBe("SKOPE Timeseries Service");
    });

});
