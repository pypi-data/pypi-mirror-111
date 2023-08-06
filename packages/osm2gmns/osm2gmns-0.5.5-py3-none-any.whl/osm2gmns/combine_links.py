from .classes import *
from shapely import ops


def _getNameForTheCombinedLink(ib_link):
    if ib_link.name == ib_link.ob_comb_link.name:
        return ib_link.name
    elif ib_link.name == '' and ib_link.ob_comb_link.name != '':
        return ib_link.ob_comb_link.name
    elif ib_link.name != '' and ib_link.ob_comb_link.name == '':
        return ib_link.name
    else:
        return None


def _getLinktypeForTheCombinedLink(ib_link):
    if ib_link.link_type == ib_link.ob_comb_link.link_type:
        return ib_link.link_type
    else:
        return None


def _getSpeedForTheCombinedLink(ib_link):
    if ib_link.free_speed == ib_link.ob_comb_link.free_speed:
        return ib_link.free_speed
    elif ib_link.free_speed == -1 and ib_link.ob_comb_link.free_speed != -1:
        return ib_link.ob_comb_link.free_speed
    elif ib_link.free_speed != -1 and ib_link.ob_comb_link.free_speed == -1:
        return ib_link.free_speed
    else:
        return None


def _checkLinkAttr(ib_link, ob_link):
    if ib_link.name != ob_link.name: return False
    if ib_link.link_type != ob_link.link_type: return False
    if ib_link.is_link != ob_link.is_link: return False
    if ib_link.free_speed != ob_link.free_speed: return False
    if ib_link.allowed_uses != ob_link.allowed_uses: return False
    if (ib_link.lanes is None and ob_link.lanes is not None) or (ib_link.lanes is not None and ob_link.lanes is None): return False
    if ib_link.from_bidirectional_way != ob_link.from_bidirectional_way: return False
    return True


def _newLinkFromLinks(link_id, up_link, down_link):
    link = Link()
    link.osm_way_id = f'{up_link.osm_way_id};{down_link.osm_way_id}'
    link.link_id = link_id
    link.name = up_link.name
    link.link_class = up_link.link_class
    link.link_type_name = up_link.link_type_name
    link.link_type = up_link.link_type
    link.is_link = up_link.is_link
    link.free_speed = up_link.free_speed
    link.allowed_uses = up_link.allowed_uses
    link.from_bidirectional_way = up_link.from_bidirectional_way

    link.from_node = up_link.from_node
    link.to_node = down_link.to_node
    link.from_node.outgoing_link_list.remove(up_link)
    link.to_node.incoming_link_list.remove(down_link)
    link.from_node.outgoing_link_list.append(link)
    link.to_node.incoming_link_list.append(link)

    link.geometry = ops.linemerge([up_link.geometry, down_link.geometry])
    link.geometry_xy = ops.linemerge([up_link.geometry_xy, down_link.geometry_xy])
    link.length = up_link.length + down_link.length

    up_lanes_list, down_lanes_list = up_link.lanes_list, down_link.lanes_list
    new_down_link_lanes_change_point_list = [point + up_link.length for point in down_link.lanes_change_point_list]
    if up_lanes_list[-1] == down_lanes_list[0]:
        link.lanes_list = up_lanes_list + down_lanes_list[1:]
        link.lanes_change_point_list = up_link.lanes_change_point_list + new_down_link_lanes_change_point_list
    else:
        link.lanes_list = up_lanes_list + down_lanes_list
        link.lanes_change_point_list = up_link.lanes_change_point_list + [up_link.length] + new_down_link_lanes_change_point_list
    link.lanes = link.lanes_list[0]
    return link


def _combLinks(network):

    removal_node_set = set()
    removal_link_set = set()

    for node_id, node in network.node_dict.items():
        if node.osm_highway and 'traffic_signals' in node.osm_highway: continue

        if len(node.incoming_link_list) != 1 or len(node.outgoing_link_list) != 1:
            continue

        ib_link, ob_link = node.incoming_link_list[0], node.outgoing_link_list[0]
        if ib_link.from_node is ob_link.to_node:
            continue

        if (ib_link.ctrl_type is not None) or (ob_link.ctrl_type is not None):
            continue

        if not _checkLinkAttr(ib_link, ob_link):
            continue

        node.valid = False
        removal_node_set.add(node.node_id)

        new_link = _newLinkFromLinks(network.max_link_id, ib_link, ob_link)
        network.link_dict[new_link.link_id] = new_link
        network.max_link_id += 1
        ib_link.valid = False
        ob_link.valid = False
        removal_link_set.add(ib_link.link_id)
        removal_link_set.add(ob_link.link_id)

    for node_id in removal_node_set: del network.node_dict[node_id]
    for link_id in removal_link_set: del network.link_dict[link_id]


def _generateSegments(network):
    segment_list = []
    max_segment_id = network.max_segment_id
    for link_id, link in network.link_dict.items():
        number_of_lanes_change_points = len(link.lanes_change_point_list)
        if number_of_lanes_change_points == 0: continue

        for i in range(number_of_lanes_change_points-1):
            segment = Segment()
            segment.segment_id = max_segment_id
            segment.link = link
            segment.start_lr = link.lanes_change_point_list[i]
            segment.end_lr = link.lanes_change_point_list[i+1]
            segment.l_lanes_added = link.lanes_list[i+1] - link.lanes
            segment_list.append(segment)
            max_segment_id += 1

        segment = Segment()
        segment.segment_id = max_segment_id
        segment.link = link
        segment.start_lr = link.lanes_change_point_list[-1]
        segment.end_lr = link.length
        segment.l_lanes_added = link.lanes_list[-1] - link.lanes
        segment.r_lanes_added = 0
        segment_list.append(segment)
        max_segment_id += 1
    network.segment_list += segment_list
    network.max_segment_id = max_segment_id


def combineShortLinks(network):
    network.link_combined = True
    _combLinks(network)
    _generateSegments(network)
