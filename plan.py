import os


class Vehicle:
    def __init__(self, **initial):
        self.speed = initial['speed']
        self.staffs = initial['staffs']
        self.maintenance_fees = initial['maintenance']
        self.cost = initial['cost']
        self.fuel = initial['fuel']

        self.time_stamp = 0
        self.time_line = []
        self.distance = 0
        self.magazine = 1

    def add_to_timeline(self, typ, time, distance):
        self.time_line.append((typ, time, distance))

    def empty(self):
        res = True
        if self.magazine == 1:
            res = False
        return res


class Transport(Vehicle):
    pass


class Launch(Vehicle):
    def __init__(self, num, **initial):
        super().__init__(**initial)
        self.state = 'free'
        self.number = num

    def finished(self):
        res = False
        if self.state == 'finished':
            res = True
        return res

    def free(self):
        res = False
        if self.state == 'free':
            res = True
        return res


class Transfer(Vehicle):
    def __init__(self, **initial):
        super().__init__(**initial)
        self.current_task = None
        self.time_remaining = 0
        self.wait = False

    def tick(self, current_second):
        if self.current_task is not None:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                if self.current_task.type == 'trans':
                    self.current_task.target.state = 'finished'
                    self.magazine = 0
                if self.current_task.type == 'load':
                    self.magazine = 1
                    self.wait = False
                tmp_time = self.current_task.target.time_stamp
                self.current_task.target.time_stamp = current_second
                self.current_task.target.add_to_timeline(TRANSFER, current_second - tmp_time, 0)
                self.current_task = None

    def busy(self):
        res = False
        if self.current_task is not None:
            res = True
        return res

    def start_next(self, task):
        global remaining_missile
        self.current_task = task
        self.time_remaining = task.required_time
        if task.type != 'load':
            remaining_missile -= 1


class Task:
    def __init__(self, typ, target):
        self.type = typ
        self.target = target
        self.required_time = None

    def set_time(self, time):
        self.required_time = time


def all_finished(launches):
    res = True
    for launch in launches:
        if not launch.finished():
            res = False
            break
    return res


def all_free(transfers):
    res = True
    for transfer in transfers:
        if transfer.busy():
            res = False
            break
    return res


def transfer_process(launches, transfers, transports):
    launches.sort(key=lambda x: x.time_stamp)
    current_second = launches[0].time_stamp
    task_queue = []
    while True:

        for launch in launches:
            if launch.time_stamp <= current_second and launch.free():
                launch.state = 'busy'
                task = Task('trans', launch)
                task_queue.append(task)

        for transfer in transfers:
            if not transfer.busy() and transfer.empty() and transports and not transfer.wait:
                task = Task('load', transfer)
                task_queue.append(task)
                transfer.wait = True

        if all_finished(launches) and not task_queue and all_free(transfers):
            break

        transfers.sort(key=lambda x: x.magazine, reverse=True)

        for transfer in transfers:
            if task_queue and not transfer.busy():
                task = task_queue[0]
                if task.type == 'trans':
                    task = task_queue.pop(0)
                    if transfer.empty():
                        task.set_time(TRANSPORT2LAUN)
                        transports.pop()
                    else:
                        task.set_time(TRANSFER2LAUN)
                elif task.type == 'load':
                    if transfer.empty():
                        task = task_queue.pop(0)
                        task.set_time(TRANSPOR2TRANSFER)
                    else:
                        continue
                    if transports:
                        transports.pop()
                    else:
                        continue
                transfer.start_next(task)

            transfer.tick(current_second + 1)

        current_second += 1

    delete_transfers = []
    for transfer in transfers:
        if transfer.empty():
            delete_transfers.append(transfer)
    for del_trans in delete_transfers:
        transfers.remove(del_trans)

    for launch in launches:
        launch.state = 'free'

    return


def simulate_once(launches, transfers, transports, routes_dict, i, res):
    global remaining_missile
    for launch in launches:
        routes = routes_dict[launch.number][i]
        laun_index = routes.index((LAUNCH, 0))
        routes1 = routes[:laun_index + 1]

        for typ, distance in routes1:
            if typ == MOVE:
                time = distance / launch.speed
            elif typ == LAUNCH:
                time = LAUNCH_TIME

            launch.time_stamp += time
            launch.distance += distance
            launch.add_to_timeline(typ, time, distance)

    launches.sort(key=lambda x: x.time_stamp)
    tmp = len(launches) - remaining_missile
    if tmp > 0:
        for i in range(tmp):
            res_launch = launches.pop()
            res.append(res_launch)

    if launches:
        for launch in launches:
            routes = routes_dict[launch.number][i]
            laun_index = routes.index((LAUNCH, 0))
            routes2 = routes[laun_index + 1:]

            for typ, distance in routes2:
                time = distance / launch.speed
                launch.time_stamp += time
                launch.distance += distance
                launch.add_to_timeline(typ, time, distance)

        transfer_process(launches, transfers, transports)


def create_plans(missile_total):
    res = []
    for laun_num in range(1, missile_total + 1):
        if laun_num < missile_total:
            for transfer_num in range(1, min(laun_num + 1, missile_total - laun_num + 1)):
                transport_num = missile_total - laun_num - transfer_num
                res.append((laun_num, transfer_num, transport_num))
        elif laun_num == missile_total:
            res.append((laun_num, 0, 0))

    return res


def create_routes(missile_total, initial_routes):
    routes_dict = {}
    key = 0
    for laun_route in initial_routes:

        if len(laun_route) < missile_total:
            repeat_times = missile_total - len(laun_route)
            template = laun_route[-1]
            for i in range(repeat_times):
                laun_route.append(template)

        routes_dict[key] = laun_route
        key += 1

    return routes_dict


def simulate(missile_total, initial_routes):
    os.remove('result')
    plans = create_plans(missile_total)
    routes_dict = create_routes(missile_total, initial_routes)

    for laun_num, transfer_num, transport_num in plans:
        launches = [Launch(i, **launch_para) for i in range(laun_num)]
        transfers = [Transfer(**transfer_para) for _ in range(transfer_num)]
        transports = [Transport(**transport_para) for _ in range(transport_num)]
        global remaining_missile
        remaining_missile = len(transfers) + len(transports)

        i = 0
        res = []
        while launches:
            simulate_once(launches, transfers, transports, routes_dict, i, res)
            i += 1

        with open('result', 'a', encoding='utf-8') as f:
            line = 'launch: ' + str(laun_num) + ' transfer: ' + str(transfer_num) + ' transport: ' + str(
                transport_num) + '\n'
            f.write('-----------------------------------------------\n' + line)
            for item in res:
                line = str(item.number) + '\t' + str(item.time_line) + '\n'
                f.write(line)


MOVE = 1
LAUNCH = 2
TRANSFER = 3

LAUNCH_TIME = 5
TRANSFER2LAUN = 5
TRANSPORT2LAUN = 5
TRANSPOR2TRANSFER = 5
remaining_missile = 0

launch_para = {'speed': 10, 'staffs': 4, 'maintenance': 5,
               'cost': 10, 'fuel': 5}
transfer_para = {'speed': 2, 'staffs': 3, 'maintenance': 6,
                 'cost': 8, 'fuel': 6}
transport_para = {'speed': 1, 'staffs': 3, 'maintenance': 6,
                  'cost': 8, 'fuel': 6}

routes11 = [[(MOVE, 10), (MOVE, 20), (LAUNCH, 0), (MOVE, 20), (MOVE, 10)]]
routes22 = [[(MOVE, 20), (MOVE, 40), (LAUNCH, 0), (MOVE, 20), (MOVE, 40)],
            [(MOVE, 20), (MOVE, 40), (LAUNCH, 0), (MOVE, 20), (MOVE, 40)]]

initial_routes = [routes11, routes22, routes11, routes11, routes11]

simulate(5, initial_routes)
