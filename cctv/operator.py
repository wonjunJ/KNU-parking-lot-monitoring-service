from apscheduler.schedulers.background import BackgroundScheduler
from . import views
from pklot import utils

import logging
logger = logging.getLogger(__name__)


def job():
    #TODO: DB 에서 가져오기
    building_list = [415, 416, 417, 420]

    for bnum in building_list:
        views.execute_detect_py(bnum)

        result_path = f'YOLO_model/yolov5/runs/detect/{str(bnum)}/result/labels/{str(bnum)}.txt'

        # empty 지우기
        utils.change_file(bnum)

        # 중심점
        if bnum == 415 or bnum == 417:
            # 결과파일
            utils.update_pklocation(utils.read_rows_from_file(result_path), bnum)
        elif bnum == 416:
            utils.adjacent_priority_algorithm(utils.read_rows_from_file(result_path), bnum)
        elif bnum == 420:
            result_path1 = f'YOLO_model/yolov5/runs/detect/{str(bnum)}/result/labels/{str(bnum)}_1.txt'
            utils.adjacent_priority_algorithm(utils.read_rows_from_file(result_path1), bnum)

            result_path2 = f'YOLO_model/yolov5/runs/detect/{str(bnum)}/result/labels/{str(bnum)}_2.txt'
            utils.update_pklocation(utils.read_rows_from_file(result_path2), bnum)
            utils.adjacent_priority_algorithm(utils.read_rows_from_file(result_path2), bnum)



def start():
    scheduler = BackgroundScheduler()

    logger.info("Added job 'execute_detection'.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()

    scheduler.add_job(job, 'interval', minutes=5, id="execute_detection")
