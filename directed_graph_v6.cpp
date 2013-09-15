// classes example
#include <iostream>
#include <string> 
#include <vector> 
#include <stdint.h>
#include <map>
#include <utility>
#include <algorithm>
#include <set>
#include <stack>
#include <queue>
#include <cassert>
#include <sstream>

/*
sample
1 won against 2
2 lost to 3
3 won against 1

p1 won against p2
p2 lost to p3
p3 won against p1

*/
using namespace std;



struct NodeType {
    string distance;
    NodeType( string d ) { distance = d; }
};

struct EdgeType  {
    int weight;
    NodeType *link;
    EdgeType( int w, NodeType *l ) { weight = w; link = l; }
};

typedef struct NodeType node;

int nodes_counter =0;
std::vector< NodeType > nodes;
std::multimap< NodeType *, EdgeType > edges;
NodeType * curr_nodes = (struct NodeType *)malloc(sizeof(node));;
NodeType * last_nodes(0);

//std::vector< NodeType > found_nodes;
std::vector< std::vector <NodeType>> v_nodes;
std::vector< std::vector <NodeType>> v_nodes_result;

template< typename T > using adjacency_list_type = std::map< T, std::vector<T> > ;

//TODO : rt CHANGED
typedef string node_type ; // for exposition
typedef adjacency_list_type<node_type> adjacency_list ;


// input of pairs of adjacent vertices of a directed graph
// 1 7 => edge from 1 -------> 7
// 2 7 => edge from 2 -------> 7
// 1 5 => edge from 1 -------> 5
// etc.


adjacency_list create( std::istream& stm )
{
    adjacency_list graph ;
    node_type a, b ;
    while( stm >> a >> b ) { graph[a].push_back(b) ; graph[b] ;}
    return graph ;
}

template< typename STACK_OR_QUEUE, typename NEXT_FN >
bool graph_search_orig( const adjacency_list& graph, node_type start, node_type target,
                    NEXT_FN next )
{
    STACK_OR_QUEUE stk_or_queue ;
    std::set<node_type> visited ;
    stk_or_queue.push(start) ;
    while( !stk_or_queue.empty() )
    {
        node_type id = next(stk_or_queue) ;
        std::cout << id << ' ' ;

        visited.insert(id) ;
        if( id == target ) { 
		std::cout << " found target\n" ; return true ; 
	}
        else
        {
            stk_or_queue.pop() ;
            auto iter = graph.find(id) ;
            if( iter != graph.end() )
                for( auto& n : iter->second )
                    if( visited.find(n)==visited.end() ) stk_or_queue.push(n) ;
        }
    }
    std::cout << "  could not find target\n" ;
    return false ;
}

template< typename STACK_OR_QUEUE, typename NEXT_FN >
bool graph_search( const adjacency_list& graph, node_type start, node_type target,
                    NEXT_FN next )
{
    //rt
    std::vector< NodeType > found_nodes;

    STACK_OR_QUEUE stk_or_queue ;
    std::set<node_type> visited ;
    stk_or_queue.push(start) ;
    while( !stk_or_queue.empty() )
    {
        node_type id = next(stk_or_queue) ;
//        std::cout << id << ' ' ;

	//rt
	found_nodes.reserve(1);
	found_nodes.push_back( NodeType(id) );

        visited.insert(id) ;
        if( id == target ) { 
		//rt
		v_nodes.reserve(1);
		v_nodes.push_back( found_nodes );

		//std::cout << " found target\n" ; 
		return true ; 
	}
        else
        {
            stk_or_queue.pop() ;
            auto iter = graph.find(id) ;
            if( iter != graph.end() )
                for( auto& n : iter->second )
                    if( visited.find(n)==visited.end() ) stk_or_queue.push(n) ;
        }
    }
    //std::cout << "  could not find target\n" ;
    return false ;
}


bool depth_first_search_orig( const adjacency_list& graph, node_type start, node_type target )
{
    return graph_search< std::stack<node_type> >( graph, start, target,
                        []( const std::stack<node_type>& stk ) { return stk.top() ; } ) ;
}

bool depth_first_search( const adjacency_list& graph, node_type start, node_type target )
{
    return graph_search< std::stack<node_type> >( graph, start, target,
                        []( const std::stack<node_type>& stk ) { return stk.top() ; } ) ;
}

bool breadth_first_search( const adjacency_list& graph, node_type start, node_type target )
{
    return graph_search< std::queue<node_type> >( graph, start, target,
                        []( const std::queue<node_type>& q ) { return q.front() ; } ) ;
}



bool topological_sort( const adjacency_list& graph )
{

	int total_nodes=0;
	//rt
	curr_nodes = NULL ;
	last_nodes = NULL ;
	
	//TODO: rt CHANGED
	std::map< node_type, int > num_pred_map ;
	for( const auto& pair : graph )
	{
		 num_pred_map[pair.first] ;
		 for( auto n : pair.second ) ++num_pred_map[n] ;
	}
	while( !num_pred_map.empty() )
	{
		bool cyclic = true ;
		for( auto iter = num_pred_map.begin() ; iter != num_pred_map.end() ;  )
		{
			if( iter->second == 0 )
			{
				//rt
				nodes.reserve(1);
				nodes.push_back( NodeType(iter->first) );
				//if (curr_nodes != NULL){
					//last_nodes = &nodes[nodes_counter-1] ; 
					//std::cout << std::endl;
					//std::cout << "last_nodes .."  << last_nodes->distance << std::endl ;					
					//std::cout << "curr_nodes .."  << iter->first << "  " << curr_nodes->distance << (nodes.at(nodes_counter)).distance  << std::endl ;					
				//}
				curr_nodes = &nodes[nodes_counter] ;
				//curr_nodes = &nodes.at(nodes_counter) ;
				nodes_counter += 1 ;

				total_nodes++;
				//std::cout << iter->first << "  " ;
				for( auto& v : graph.find(iter->first)->second )
					 --num_pred_map[v] ;
				iter = num_pred_map.erase(iter) ;
				cyclic = false ;
			}
			else ++iter ;
		}
		if(cyclic)
		{
			std::cerr << "graph is cyclic - nodes " ;
			for( auto& pair : num_pred_map ) std::cout << pair.first << ' ' ;
			std::cout << '\n' ;
			return false ;
		}
	}
	std::cout << '\n' ;

	//print all nodes
	std::cout << "==================================================" << std::endl ;
	std::cout << "===========O U T P U T============================" << std::endl ;
	std::cout << "==================================================" << std::endl ;
	int i=0;
	for (std::vector<NodeType>::iterator it = nodes.begin() ; it != nodes.end(); ++it,++i) {
		for (int j=i ; j < nodes.size() ; ++j){
		 	//std::cout << " [" << i << "," << j << "] ";		
			//std::cout << "======================" << std::endl ;
		 	//std::cout << " [" << nodes.at(i).distance << "," << nodes.at(j).distance << "] ";		
			//std::cout << "DFS " << nodes.at(i).distance <<" to " << nodes.at(j).distance << "=> " ; 
			depth_first_search( graph, nodes.at(i).distance, nodes.at(j).distance ) ;
			//std::cout << " [" << nodes.at(j).distance << "," << nodes.at(i).distance << "] ";	
			//std::cout << "DFS " << nodes.at(j).distance <<" to " << nodes.at(i).distance << "=> " ; 
			depth_first_search( graph, nodes.at(j).distance, nodes.at(i).distance ) ;
			//std::cout << "======================" << std::endl ;
		}
	}
	//std::cout << '\n';
	//std::cout << nodes.begin()->distance << "  -- "<< nodes_counter << " done.." << std::endl ;

	//std::cout << "Total Nodes = " << total_nodes << std::endl ;	
	//std::cout << "Re-Visit All the found targets..." << std::endl;
	i=0;

	//std::cout << "*******" << std::endl;
	//std::cout << v_nodes[0][0].distance;

	//std::cout << "Total size = " << v_nodes.size() << std::endl;
	//rt
	std::vector< NodeType > found_nodes_result;
/*
	for (std::vector<std::vector<NodeType>>::iterator v_it = v_nodes.begin() ; v_it != v_nodes.end(); ++v_it,++i) {
		std::cout << "size of current nodes list=" << v_it[0].size()  << std::endl;
		for (int j=0 ; j< v_it[0].size() ; ++j) {
			//std::cout << (v_nodes[0][j]).distance << " "   ;
			//std::cout << i << "," << j  << "=" << v_nodes[i][j].distance << "   "  ;
			std::cout << v_nodes[i][j].distance << "   "  ;
		}
		std::cout << std::endl ;
	}
*/

	i=0;
	for (std::vector<std::vector<NodeType>>::iterator v_it = v_nodes.begin() ; v_it != v_nodes.end(); ++v_it,++i) {
		//std::cout << "size of current nodes list=" << v_it[0].size()  << std::endl;
		if ( v_it[0].size() >= 2 /*total_nodes*/ ) {
			for (std::vector<NodeType>::iterator it = v_it[0].begin() ; it != v_it[0].end(); ++it) {
			//for (int j=0 ; j< v_it[0].size() ; ++j) {
				//std::cout << (v_nodes[0][j]).distance << " "   ;
				//std::cout << i << "," << j  << "=" << v_nodes[i][j].distance << "   "  ;
				//std::cout << v_nodes[i][j].distance << "   "  ;
				std::cout << it->distance << "  " ;
			}
			std::cout << std::endl ;
		}
	}


	std::cout << "==================================================" << std::endl ;
	//printed all nodes

	return true ;
}

/*
int main_orig() // trivial test driver
{
    const std::string str = "1 2   1 7   1 8   2 3   2 6   2 10  3 4   3 5   3 11   "
                      "6 10   6 12  8 9   8 12   9 10   9 11   11 7   12 5" ;

    std::istringstream stm(str) ;
    adjacency_list graph = create(stm) ;

    std::cout << "top sort => " ; topological_sort(graph) ;
    std::cout << "DFS 1 to 5 => " ; depth_first_search( graph, 1, 5 ) ;
    std::cout << "BFS 1 to 5 => " ; breadth_first_search( graph, 1, 5 ) ;
    std::cout << "DFS 1 to 6 => " ; depth_first_search( graph, 1, 6 ) ;
    std::cout << "BFS 1 to 6 => " ; breadth_first_search( graph, 1, 6 ) ;
    std::cout << "BFS 1 to 6 => " ; breadth_first_search( graph, 1, 12 ) ;

}
*/
int main_input(string str) // trivial test driver
{
    //const std::string str = "1 2   1 7   1 8   2 3   2 6   2 10  3 4   3 5   3 11   "
    //                  "6 10   6 12  8 9   8 12   9 10   9 11   11 7   12 5" ;

    //const std::string str = "1 2   1 7   1 8   2 3   2 6  3 4   3 5   3 11   "
    //                  "6 10   6 12  8 9   8 12   9 10   9 11   11 7   12 5   5 10   9 7   12 7   7 1" ;

    //const std::string str = "1 2   3 2   3 1" ;

    std::istringstream stm(str) ;
    adjacency_list graph = create(stm) ;

    //std::cout << "top sort => " ; 
    topological_sort(graph) ;
    //std::cout << "DFS 1 to 5 => " ; depth_first_search( graph, 1, 5 ) ;
    //std::cout << "BFS 1 to 5 => " ; breadth_first_search( graph, 1, 5 ) ;
/*
    std::cout << "DFS 1 to 6 => " ; depth_first_search( graph, 1, 6 ) ;
    std::cout << "BFS 1 to 6 => " ; breadth_first_search( graph, 1, 6 ) ;
    std::cout << "BFS 1 to 6 => " ; breadth_first_search( graph, 1, 12 ) ;
*/
}


static inline std::string &trimAll(std::string &s)
{   
    if(s.size() == 0)
    {
        return s;
    }

    int val = 0;
    for (int cur = 0; cur < s.size(); cur++)
    {
        if(s[cur] != ' ' && std::isalnum(s[cur]))
        {
            s[val] = s[cur];
            val++;
        }
    }
    s.resize(val);
    return s;
}


string strip(const string& s, const string& chars=" ") {
    size_t begin = 0;
    size_t end = s.size()-1;
    for(; begin < s.size(); begin++)
        if(chars.find_first_of(s[begin]) == string::npos)
            break;
    for(; end > begin; end--)
        if(chars.find_first_of(s[end]) == string::npos)
            break;
    return s.substr(begin, end-begin+1);
}

int main () {
	std::string graph_string="";
	std::string graph_delimiter="    ";
	std::vector<string> match_results1;
        /*
                inputs and parse the same
        */
        std::string d1 = "won against" ;
        std::string d2 = "lost to" ;

	std::string input;
	std::cout << 	"Help"
			" 	: Type [ done ] when all inputs user have provided result of each match." << std::endl ; 
	while(true){
		getline(cin, input);
		
		if(input == "done")
			break;
		else{
			match_results1.reserve(1);
			match_results1.push_back(input);
		}
			
	}

	for (std::vector<string>::iterator it = match_results1.begin() ; it != match_results1.end(); ++it) {
		string match_result = *it;
		string node1 , node2;
                string s = match_result ;
                string s2 = match_result ;
                size_t pos = 0;
                std::string token;
                while ((pos = s.find(d1)) != std::string::npos) {
                        token = s.substr(0, pos);
                        node1=strip(token) ;
                        s.erase(0, pos + d1.length());
                }

                while ((pos = s.find(d2)) != std::string::npos) {
                        token = s.substr(0, pos);
			node1=strip(token) ;
                        s.erase(0, pos + d2.length());
                }

                node2 = strip(s);
                if ((pos = s2.find(d1)) != std::string::npos) {
			graph_string = graph_string + graph_delimiter + node1 + " " + node2 ;
                }

                if ((pos = s2.find(d2)) != std::string::npos) {
			graph_string = graph_string + graph_delimiter + node2 + " " + node1 ;
                }
                

	}

	//std::cout << graph_string << std::endl;
	std::cout << "Processing...." << std::endl;
	//graph_string="1 2   3 2   3 1";
	main_input(graph_string);
  return 0;

}


